#!/usr/bin/env python3
"""Read-only structural check for one archived day. It cannot verify factual accuracy."""
import argparse
import json
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--day", type=int, required=True)
    parser.add_argument("--log", help="旧日或非状态 last_log 的相对路径")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    errors = []
    try:
        state = json.loads((root / "旅行状态.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": ["状态 JSON 无法读取: " + str(exc)]}, ensure_ascii=False, indent=2))
        return 2
    if args.log:
        log = root / args.log
    elif state.get("last_completed_day") == args.day and state.get("last_log"):
        log = root / state["last_log"]
    else:
        print(json.dumps({"ok": False, "errors": ["旧日请用 --log 指定主日志相对路径"]}, ensure_ascii=False, indent=2))
        return 2
    prefix = f"第{args.day:02d}天_"
    if not log.is_file() or not log.name.startswith(prefix):
        errors.append("主日志不存在或序号不符")
        text = ""
    else:
        text = log.read_text(encoding="utf-8-sig")
    city = log.parent
    for filename in [f"第{args.day:02d}天_来源记录.json", f"第{args.day:02d}天_归档核验记录.md", "目录.md"]:
        if not (city / filename).is_file():
            errors.append("缺少 " + str(city / filename))
    src = city / f"第{args.day:02d}天_来源记录.json"
    if src.is_file():
        try:
            data = json.loads(src.read_text(encoding="utf-8-sig"))
            if data.get("day") != args.day or not data.get("sources"):
                errors.append("来源 JSON 缺少当天序号或来源列表")
        except ValueError:
            errors.append("来源 JSON 无法解析")
    if text:
        if "# 题注" not in text or "## 参考文献" not in text:
            errors.append("主日志缺少题注或参考文献")
        refs = [int(x) for x in re.findall(r"^\[(\d+)\]\s", text, re.MULTILINE)]
        if not refs or refs != list(range(1, len(refs) + 1)):
            errors.append("参考文献编号不连续")
        for local in re.findall(r"!\[[^]]*\]\((\./[^)]+)\)", text):
            if not (city / local).is_file():
                errors.append("本地图片不存在: " + local)
        for word in ["唯一住宿", "示意图", "待核"]:
            if word not in text:
                errors.append("缺少关键标记: " + word)
        if (city / "目录.md").is_file() and log.name not in (city / "目录.md").read_text(encoding="utf-8-sig"):
            errors.append("地方目录未链接主日志")
        if (root / "目录.md").is_file() and log.name not in (root / "目录.md").read_text(encoding="utf-8-sig"):
            errors.append("总目录未链接主日志")
    print(json.dumps({"ok": not errors, "day": args.day, "log": str(log), "errors": errors,
                      "scope": "仅结构校验；文献、图片、路况、统计口径需人工复核"}, ensure_ascii=False, indent=2))
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
