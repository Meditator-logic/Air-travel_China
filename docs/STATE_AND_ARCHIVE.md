# 状态与归档格式

## 状态机

| 状态 | 含义 | 自动新日志 |
|---|---|---|
| `planned` | 已设计，尚未获用户启动 | 禁止 |
| `active` | 正在逐日推进 | 日期门禁通过才可 |
| `paused` | 暂停，保留路线 | 禁止 |
| `completed` | 抵达必须返回的终点 | 禁止 |
| `terminated` | 提前结束，记录真实终点 | 禁止 |

状态文件使用 UTF-8 JSON。日期用 `YYYY-MM-DD`，时区固定 `Asia/Shanghai`。`last_completed_day` 是已归档日志序号，和日历过去了几天不同。`next_day = last_completed_day + 1`。修订旧篇不增加旅行序号。

## 必备字段

`journey_id`、`journey_status`、`start_anchor`、`required_end_anchor`、`macro_corridor`、`estimated_total_days`、`estimated_remaining_days`、`current_stage`、`next_macro_checkpoint`、`next_five_anchors`、`closed_counties`、`recent_counties`、`days_in_current_county`、`days_at_current_settlement`、`route_deviation_reason`、`last_route_audit`、`next_route_audit_day`、`last_completed_day`、`last_completed_log_date`、`last_log`、`next_day`、`current_overnight_anchor`、`route_outline`。

`next_five_anchors` 恰有五项，每项至少有 `planned_day`、`province`、`settlement` 和主题；第一项的 `planned_day` 应等于 `next_day`。为兼容当前历史归档，县级市、地级市可能用不同的 `county` 名称；续写时应在路线审计里说明比较层级，不用字符串不等代替地理判断。

## 目录约定

```text
PROJECT_ROOT/
  旅行状态.json
  目录.md
  路线总纲_当前旅程.md
  省份/
    城市或住宿聚落/
      目录.md
      第NN天_出发地至住宿地_主题.md
      第NN天_来源记录.json
      第NN天_归档核验记录.md
      媒体/第NN天/
        路线图.svg（真实底图优先，含指北针与方向箭头）
        来源资料和经核验的图像
```

首次运行可复制本仓库的 `templates/目录.example.md` 创建根目录；每天新建地方 `目录.md`。`templates/来源记录.example.json` 和 `templates/归档核验记录.example.md` 只展示结构，使用时须填真实来源与核验结果，不可原样算作完整归档。

主日志中的本地图片路径相对主日志所在目录。发给用户的本地链接需使用**完整绝对路径**，如 Windows 下的 `[打开日志](<F:/你的目录/第06天_主题.md>)` 或 Linux 下的 `[打开日志](/home/user/travel/第06天_主题.md)`；GitHub 仓库内部链接使用相对路径。不要把本机绝对路径硬编码到可移植提示词。

## 来源记录

来源 JSON 应有 `schema_version`、`journey_id`、`day`、`accessed_at`、`sources`、`limitations`。每条来源至少记录编号、机构、标题、URL；本地副本仅在确实保存时填写。图片另记原图 URL、来源页、作者/机构、页面日期、已知拍摄日期、许可或使用限制。路线模型注明端点仅为研究参考点。

## 归档事务顺序

1. 检查同日同序号是否已有完整归档，防止覆盖。
2. 写媒体、来源、主日志和地方目录；验证引用编号、本地图片、JSON、唯一夜宿，以及路线图的指北针与行进方向箭头是否齐备；驻留日另验城内景点行程图（编号景点+先后箭头）与逐景点导览表是否完整。
3. 写归档核验记录并更新根目录。
4. 最后用临时文件写新状态，再原子替换 `旅行状态.json`；替换前再次确认原状态没有被另一进程推进。归档核验记录不要预先写入尚未生成的新状态哈希。状态写入后可追加一次状态一致性复核，不得因此再增加旅行日。
5. 若任何步骤失败，状态仍停在原 `next_day`。重试时补齐同一日归档，不增加旅行日。

本仓库脚本进行结构检查，不能证明文献真实性、图片许可、路况或写作质量；这些仍需 agent 阅读原文并人工抽查。不要让两个自动任务同时写一个状态文件。
