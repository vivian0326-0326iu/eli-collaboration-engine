# 技术事实与宣传边界（2026-10-16）

这是一个公开的**可按步骤复刻的配置与工作流仓库**，不是 Mac MCP 或 Codex 的再发行版，也没有绕过 ChatGPT 账号权限。外部上游文档更新后应重新审核。

| 论断 | 结论 | 主要依据 |
|---|---|---|
| Mac MCP 可以与 Codex 原生代理协作、调用 `spawn_agent`、延续 provider-native session | 上游公开支持；读者仍须现场验证登录/工具权限 | [Mac MCP Agents and Scheduled Tasks](https://github.com/bulutarkan/mac-mcp/blob/main/docs/agents-and-tasks.md) |
| Mac MCP 的受限写入 Git 隔离工作树可显式 apply | 上游具备隔离与冲突保护，真实能力以当前版本为准 | 同上，Isolated Git worktrees |
| macOS 初次安装 Mac MCP | 官方提供 Releases 安装包及多种方式 | [Mac MCP README](https://github.com/bulutarkan/mac-mcp) |
| 完整自定义 MCP 能在任意普通 ChatGPT 个人账号使用 | **不能这么声称**。完整写入功能有套餐/工作区/界面资格约束；个人实际可用不代表通用 | [OpenAI Connecting custom MCP servers in ChatGPT](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) |
| 普通 Chat 可无需认证直连本机 localhost | **不能**。ChatGPT 要求受支持的远程 MCP/安全隧道，且服务需认证 | 同上、[Mac MCP](https://github.com/bulutarkan/mac-mcp) |
| Agent Skills 用 `SKILL.md` 目录发布 | 符合 Codex 技能结构；读取不等于能访问 Mac MCP | [OpenAI Codex Skills](https://developers.openai.com/codex/skills) |
| 只要关掉普通聊天 AI 就能 24×7 自行干活 | **未实现**；Mac MCP Scheduled Tasks 是独立、需要配置/批准的实验性功能 | [Mac MCP Agents and Scheduled Tasks](https://github.com/bulutarkan/mac-mcp/blob/main/docs/agents-and-tasks.md) |
| GitHub 发布能放 README / Skill / ZIP release | 已有官方 GitHub 文档支持 | [GitHub Repository Quickstart](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories)、[Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) |
| “这种协作一定省 90% / 无限免费” | **没有证据，不能宣传**。作者只完成具体小型项目和主控/执行器的角色优化，未做同条件的账户账单/用量对照 | 项目内部历史验收（仅作作者经历） |
| 原作者私有系统 108 项测试通过 | **有历史 Git 记录**；不是本仓库测试成绩、也不是每个读者的运行结果 | 作者原私有交接记录，不随公开包发布 |

## 如何描述公开复刻包的测试

- `python3 -m unittest discover -s tests -q` 是**公开包自身**的离线本地检查，主要核验任务记录与失败安全门，不调用模型也不连接 Mac MCP。
- `examples/bug-demo` 故意保留失败用例，只有有真实 agent 代修并在用户新 Git 项目中重新验收，才能称为演练成功。
- A-D、E-G、H 真机联通必须有**读者自己**的真实工具回执。工具缺失 / 账号没权限均应标 BLOCKED，而不是 AI 自称 PASS。
- 对任何费用，真实账户账单与主观估计分开；用量未知填 `UNKNOWN`，不能填 `0`。额外付费 API 未经许可不调用。

## 版权范围

原创的 Markdown、Python 辅助代码、示例和测试采用本目录 MIT 许可。Mac MCP 源码和 ChatGPT/Codex 产品均来自各自官方维护渠道，本包没有打包它们。项目名 **eli｜协作引擎** 仅指此开源工作流，非任何上游产品的官方合作发行版。
