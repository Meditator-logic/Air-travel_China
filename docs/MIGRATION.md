# 迁移、接续与 GitHub 发布

## 新建旅程

将本发布包复制到任意操作系统和目录，记为规则库 `RULES_ROOT`。另建运行目录 `PROJECT_ROOT`；从 `templates/` 复制示例状态、路线总纲和总目录，改写路线内容。脚本从规则库目录运行，`--root` 始终指向运行目录。初始状态必须是 `planned`，由用户明确启动后才改成 `active`。把实际 `RULES_ROOT` 与 `PROJECT_ROOT` 一起传给所用 agent 的定时系统。

最小文件准备示例（命令在规则库目录运行；路径按本机替换）：

```powershell
$travelRoot = 'F:\AITasks\Codex\新旅程'
New-Item -ItemType Directory -Path $travelRoot -Force | Out-Null
Copy-Item 'templates/旅行状态.example.json' (Join-Path $travelRoot '旅行状态.json')
Copy-Item 'templates/路线总纲.example.md' (Join-Path $travelRoot '路线总纲_当前旅程.md')
Copy-Item 'templates/目录.example.md' (Join-Path $travelRoot '目录.md')
python tools/preflight.py --root $travelRoot
```

第一次门禁应返回 `D planned`。编辑状态与路线后，用户明确启动，改为 `active`，再运行门禁，预期 `READY`。`READY` 仅表示结构与日期门禁通过，仍要核验未来五站的地理连续性与研究资料。运行目录可在其他盘符或操作系统上，不需要 `F:`。

Windows 的 `F:\AITasks\Codex\中国自驾壮游` 只是原作者的运行目录，不是跨平台前提。其他 agent 可使用 Linux 或 macOS 路径；文件中的路径统一从其 `PROJECT_ROOT` 解析。

## 接续正在运行的旅程

要从第 N 天真正接续，必须同时迁移：

1. 最新 `旅行状态.json`、根 `目录.md`、路线总纲、未来专题清单；
2. 最近至少一篇主日志及其来源记录、归档核验记录；
3. 过去行程的目录与 `closed_counties` 语义，足以核查折返冷却期；
4. 最近日志引用的本地媒体，或可访问的原始来源链接；
5. 本仓库的规范、模板和提示词。

迁移后先运行 `preflight.py`，再让新 agent 口头复述当前 `journey_status`、`next_day`、唯一夜宿地、未来五站、下一宏观检查点和已关闭区域。旧 agent 的定时任务要停止，确保只有一个写入者。**不要把本发布包的 planned 示例状态覆盖真实进度。**

## 定时任务设置

每天在北京时间选择一个固定时刻运行，例如 08:00。将 [每日执行提示词](../prompts/DAILY_AGENT.md) 作为任务正文，并随任务明确写入实际 `PROJECT_ROOT` 和 `RULES_ROOT` 的绝对路径。任务须拥有网络和文件读写能力。是否能自动运行、是否通知、如何保存执行记录取决于平台；平台功能与本仓库文件是两层配置。**仅上传 GitHub 不会自动创建定时任务。**

若平台只接受一段提示词，可将 `AGENTS.md`、两份规范、模板与状态字段说明放在 agent 可读目录，并让提示词引用这些文件。首次运行先用 planned 状态测试 D，再由用户启动并测试首篇归档。

## GitHub 公共发布范围

这个包只含原创工作流文字、模板、样例状态和校验脚本。**不默认包含**一整趟日志、第三方照片、地图瓦片、政府 PDF 副本、网页抓取、含有联系人或凭据的研究缓存。公开完整旅行日志前，逐一核对图片和材料的再发布许可；无许可时使用来源页链接与图片直链，并遵守站点规则。真实运行状态会不断变化，不建议在公开仓库与本机自动任务同时同步。

发布前运行：

```bash
python tools/preflight.py --root . --state templates/旅行状态.example.json
python -m py_compile tools/preflight.py tools/verify_archive.py
```

确认无机密或不应发布的素材后，在本发布包目录初始化并推送到自己创建的 GitHub 空仓库：

```bash
git init
git add .
git commit -m "Publish portable daily roadtrip workflow"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

这一步需要你的 GitHub 仓库地址及本机认证。上传后的 README 链接从仓库首页打开；本机 `F:` 路径不会在他人的电脑或 GitHub 上生效。
