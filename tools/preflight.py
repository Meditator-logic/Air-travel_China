#!/usr/bin/env python3
"""Read-only daily gate. Prints one JSON decision; never changes travel state."""
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def emit(decision, reason, **data):
    print(json.dumps({"decision": decision, "reason": reason, **data}, ensure_ascii=False, indent=2))
    return 2 if decision == "B" else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="运行目录 PROJECT_ROOT")
    parser.add_argument("--state", default="旅行状态.json", help="相对 root 或绝对状态文件路径")
    parser.add_argument("--today", help="覆盖北京时间日期 YYYY-MM-DD，用于演练")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    state_file = Path(args.state)
    if not state_file.is_absolute():
        state_file = root / state_file
    if not state_file.is_file():
        return emit("B", "状态文件不存在", path=str(state_file))
    try:
        state = json.loads(state_file.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return emit("B", "状态 JSON 无法读取", detail=str(exc))
    status = state.get("journey_status")
    if status not in {"planned", "active", "paused", "completed", "terminated"}:
        return emit("B", "未知 journey_status", value=status)
    if status != "active":
        return emit("D", f"旅程状态为 {status}，不得生成新日志", journey_id=state.get("journey_id"))

    required = ["journey_id", "start_anchor", "required_end_anchor", "macro_corridor",
                "estimated_total_days", "estimated_remaining_days", "current_stage", "next_macro_checkpoint",
                "next_five_anchors", "closed_counties", "recent_counties",
                "days_in_current_county", "days_at_current_settlement",
                "route_deviation_reason", "last_route_audit", "next_route_audit_day",
                "current_overnight_anchor", "last_completed_day", "last_completed_log_date",
                "last_log", "next_day", "route_outline"]
    missing = [key for key in required if key not in state]
    if missing:
        return emit("B", "活动旅程缺少必要状态字段", missing=missing)
    try:
        today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else datetime.now(timezone(timedelta(hours=8))).date()
        last = datetime.strptime(state["last_completed_log_date"], "%Y-%m-%d").date() if state["last_completed_log_date"] else None
    except (TypeError, ValueError) as exc:
        return emit("B", "日期无效", detail=str(exc))
    if state.get("timezone") != "Asia/Shanghai":
        return emit("B", "时区必须为 Asia/Shanghai")
    if state["next_day"] != state["last_completed_day"] + 1:
        return emit("B", "next_day 与 last_completed_day 不连续")
    anchors = state["next_five_anchors"]
    if not isinstance(anchors, list) or len(anchors) != 5:
        return emit("B", "next_five_anchors 必须恰有五项")
    if [a.get("planned_day") for a in anchors] != list(range(state["next_day"], state["next_day"] + 5)):
        return emit("B", "未来五站的 planned_day 与 next_day 不连续")
    if any(not a.get("province") or not a.get("settlement") for a in anchors):
        return emit("B", "未来五站缺少省份或住宿聚落")
    if not state["macro_corridor"] or not state["required_end_anchor"].get("settlement"):
        return emit("B", "宏观走廊或必须返回的终点缺失")
    if not (root / state["route_outline"]).is_file():
        return emit("B", "路线总纲不存在", path=state["route_outline"])
    if not (root / "目录.md").is_file():
        return emit("B", "总目录不存在")
    if state["last_completed_day"] > 0 and (not state["last_log"] or not (root / state["last_log"]).is_file()):
        return emit("B", "最近一篇主日志不存在", path=state["last_log"])
    if last and today < last:
        return emit("B", "当前日期早于最近完整归档日期")
    if last == today:
        log = root / state["last_log"] if state["last_log"] else None
        prefix = f"第{state['last_completed_day']:02d}天_"
        companions = [log.parent / (prefix + "来源记录.json"),
                      log.parent / (prefix + "归档核验记录.md"),
                      log.parent / "目录.md"] if log else []
        if not log or not log.is_file() or not all(p.is_file() for p in companions):
            return emit("B", "状态记为今日完成，但主日志或配套归档不完整")
        try:
            source = json.loads(companions[0].read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            return emit("B", "今日来源记录无法解析")
        if source.get("day") != state["last_completed_day"]:
            return emit("B", "今日来源记录序号与状态不符")
        return emit("C", "北京时间当天已完成；不要重复生成", day=state["last_completed_day"], log=state["last_log"])
    return emit("READY", "日期与状态门禁通过；仍需 agent 完成路线、来源和归档核验",
                next_day=state["next_day"], today=today.isoformat(),
                next_anchor=anchors[0], last_log=state["last_log"])


if __name__ == "__main__":
    raise SystemExit(main())
