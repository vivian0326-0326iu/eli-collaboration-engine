---
name: eli-collaboration-engine
description: 当用户想通过普通ChatGPT或已有Mac MCP与Codex协作做代码、Mac项目、修Bug、独立验收和持续项目恢复时使用。先验证真实工具权限与历史状态；优先同一Codex原生会话多轮反馈，不要求用户打开新的云Work。
---

# eli｜协作引擎：可执行协作 Skill

> 本 Skill 可由 **Codex** 在支持的 Skills 环境中发现；普通 ChatGPT 是否能读取或调用它取决于当前会话能力。Skill 是工作合同，不会自行安装 Mac MCP、授权账号、提供高权限工具或执行后台任务。

## 启动时

1. 先确定你在哪：ChatGPT 里的 **eli 主控**，还是 Codex **执行代理**。不要把 Codex 写成 eli，也不要假装普通 Chat 能调用未连接的 Mac MCP。
2. 阅读仓库根目录 `README.md`、`AGENTS.md` 和当前 `scripts/checkpoint.py show`。如果当前有已配置的真实工具，先只读确认。新项目从 `docs/01-从零安装.md` 开始。
3. 不把历史日志当作本次权限或计费凭证。任何重大取舍/付费/公网端点/高风险写入，必须确认当前已授权。

## 首选的闭环

1. eli 只读审查 Git 和任务来源，拆成可验收的小任务。
2. Mac MCP 查询 `agent_catalog` / `mac_mcp_panel_state` 或等价工具，核验 Codex 已登录、模型可用与访问模式。默认保留当前用户指定的高推理模型；不能使用时明确阻断或让用户选择，不偷偷更换。
3. Codex 任务设置范围与超时，有写入则优先 Git 隔离工作树、 `retries=0`。
4. 以 `get_agent` 为准收集代理终态、 `agent_id`、 `session_id`、 `workflow_id`、真实错误及工件，而不是信任代理文字自报。
5. 返回 `NEEDS_CONTROLLER:` 时，eli 给出判断，再经 `agent_action(action="message", agent_id=...)` 继续同一 **Codex provider-native session**；检测 session ID 一致。不知道副作用时禁止自动 replay。
6. 已完成变更经 eli 检查 diff 和测试、显式 apply，成功再 Git commit、记录 `checkpoint.py note` / `snapshot` / `verify`。没有实际写入、测试就不能称 PASS。

## 正式拒绝条件

- 原 ChatGPT 云 Work 线程 UUID **不等于** Codex native session；本套件不能向旧云 Work 精确定向发送消息。
- `get_agent` 的历史元数据可见 **不等于** 原生 rollout 仍可续接。`no rollout found` 停止直接重试；先辨认已生效副作用，安全接力新原生代理。
- 对带秘密的真实工作区，不自动开启公网或将凭证/连接 URL 明文写到项目档案。
- 不未经授权创建无限循环的订阅或定时后台任务；Mac MCP Scheduled Tasks 是独立功能，并非“ChatGPT 关了还会主动唤醒原会话”。
- 纯聊天、短文写作无需额外唤醒 Codex；尊重用户要求的主控/执行器角色。

## 相关参考（按需读取，不必一次性加载全部）

- `references/CHATGPT_CONTROLLER.md`：主控 ChatGPT 的全部提示词与验收门槛。
- `references/TOOL_CHECKLIST.md`：Mac MCP 真实调用的必要字段、预算和副作用。
- `../../../docs/eli-engine/03-双向协作与长期恢复.md`：跨回合恢复。

**每次交付**报告做到/未做到、测试命令与结果、Git SHA、运行时间、费用来源和未知项，保存可追溯证据。
