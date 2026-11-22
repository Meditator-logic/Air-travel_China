# Agent 工作约定

本仓库是工作流发布包，不是正在运行的旅行目录。`templates/旅行状态.example.json` 的 `planned` 状态不得擅自改为 `active`。

执行每日任务前先读 `docs/WORKFLOW.md`、`docs/STATE_AND_ARCHIVE.md`、`policies/ROUTE.md`、`policies/EDITORIAL.md`、`templates/日志模板.md` 和目标工作目录的 `旅行状态.json`、`目录.md`、当前路线总纲、最近一篇主日志。以用户给定的工作目录为准，不假定 `F:` 盘存在。

若 `journey_status` 不是 `active`，直接报告状态。若北京时间当日已经完整归档，不生成第二篇。仅执行 `next_five_anchors` 的第一项。写完全部文件并核验通过后才推进状态；失败时保留原状态并报告明确阻断。

统计、史实、地图、照片须有来源。规划草案和批准文本分开，不能把图片写成实时观察。模拟驾驶和观察必须明示。每天只有一处住宿聚落，离开已关闭县域后不自动折返。

发布到 GitHub 时，不把运行目录下的第三方媒体、网页副本、个人资料、凭据或会不断变动的真实旅行状态并入本发布包。需要共享实际旅程时，另做逐项审核的资料包。
