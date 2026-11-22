# 每日一城：中国平行时空自驾壮游

这是一套让 AI 每天交付一篇**模拟自驾调研日志**的可移植工作流。它以路线状态驱动，在有起点、检查点和终点的全国旅程中逐日推进。日志使用可追溯资料、明确的统计口径、规划图与实景照片；第一人称驾驶只表示模拟情境。

发布包整理日期：2026-11-22。`policies/ROUTE.md` 依据原路线控制规范 v1，`policies/EDITORIAL.md` 与 `templates/日志模板.md` 依据原日志规范及模板 v4；已把固定本机路径改为可配置的 `PROJECT_ROOT`。

## 先看这些文件

| 文件 | 用途 |
|---|---|
| [工作流说明](docs/WORKFLOW.md) | 从门禁、选站、调研到归档的完整操作 |
| [迁移与启动](docs/MIGRATION.md) | 新 agent、新目录、定时任务和旧旅程接续 |
| [每日执行提示词](prompts/DAILY_AGENT.md) | 贴给其他 agent 或定时任务的可移植指令 |
| [归档与状态字段](docs/STATE_AND_ARCHIVE.md) | 目录、JSON、原子推进和校验规则 |
| [第6天实操范例](docs/CASE_STUDY_DAY06.md) | 从状态门禁到来源、地图、路线和状态推进的具体过程 |
| [检索与图像细则](docs/SOURCES_AND_MEDIA.md) | 数据、规划版本、照片和引用的核验方法 |

## 五分钟启动一趟新旅程

1. 将本仓库放在一个**规则目录**；另建一个独立的 `PROJECT_ROOT` 作为**运行目录**。所有下面的 `python tools/...` 命令均从规则目录执行，`--root` 指向运行目录。
2. 将 `templates/旅行状态.example.json` 复制到 `PROJECT_ROOT/旅行状态.json`，将 `templates/路线总纲.example.md` 复制到 `PROJECT_ROOT/路线总纲_当前旅程.md`，将 `templates/目录.example.md` 复制到 `PROJECT_ROOT/目录.md`。编辑状态、路线总纲和目录，使起点、终点、宏观走廊、预计天数、未来五站和夜宿锚点一致。初始 `journey_status` 保持 `planned`。
3. 先运行 `python tools/preflight.py --root "PROJECT_ROOT"`，应返回 `D planned`。用户明确启动后，才把状态改为 `active`；再次运行应返回 `READY`。
4. 把 [每日执行提示词](prompts/DAILY_AGENT.md) 交给可联网、可读写文件的 agent。定时每天调用一次，并显式传入规则目录 `RULES_ROOT` 和运行目录 `PROJECT_ROOT`；agent 应自行取北京时间。
5. 首篇的文件和目录写齐后，用 `python tools/verify_archive.py --root "PROJECT_ROOT" --day 1 --log "省份/城市或住宿聚落/第01天_实际文件名.md"` 做结构校验。再人工抽查来源、图像和路线，**最后**推进状态。状态推进后可省略 `--log` 重跑校验。

没有 Python 也能人工执行；两个脚本只负责**结构检查**，不会自动研究地方、下载图片或更新旅行状态。

## 仓库内容

```text
AGENTS.md                       给支持仓库指令的 agent
prompts/DAILY_AGENT.md          跨平台日常提示词
policies/ROUTE.md               路线、停留和闭环规则
policies/EDITORIAL.md           研究、引用和图像规则
templates/旅行状态.example.json   安全的 planned 示例
templates/路线总纲.example.md     启动前路线设计样板
templates/目录.example.md         运行目录的总目录样板
templates/日志模板.md             每篇日志结构
templates/来源记录.example.json   来源记录结构样板
templates/归档核验记录.example.md  归档核验结构样板
tools/preflight.py              读取状态与日期门禁
tools/verify_archive.py         检查归档结构和链接
docs/                           操作、字段、迁移和发布说明
```

项目运行产生的 `旅行状态.json`、完整日志、网页副本、照片和规划 PDF **不在这个公开发布包内**。这些属于具体旅程的数据，应单独保存在工作目录中。详见 [迁移与 GitHub 发布](docs/MIGRATION.md)。

## 输出契约

每次运行只返回一个结果：**A 完整归档、B 明确阻断、C 当天已完成、D 旅程非 active**。A 必须含可直接打开的主日志链接与下一站；B 必须指明阻断原因且状态不得推进。

## 适用边界

这是虚拟研究旅行，不提供实时路况、天气、边境通行或场馆开放保证。所有实驾相关信息应在实际出发前重新核验。第三方图片、地图和规划资料由各自权利人持有；公开仓库默认只记录来源链接，不重新发布原件。
