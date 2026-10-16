# Mac MCP 工具调用检查单

工具名称和 schema 以当前连接返回为准，不要只靠这些历史示例猜工具存在。

| 阶段 | 实际接口范例 | 真实通过条件 |
|---|---|---|
| 发现 | `mac_mcp_panel_state`, `tool_discover`, `agent_catalog` | 服务与Codex provider可见；模型、推理强度、scope经确认 |
| 读取 | `get_system_info` / `list_directory` | 非秘密真实数据回执 |
| 写入 | `write_file`、`edit_file` | 独立测试目录写入再`read_file`逐字一致；若权限不足标BLOCKED |
| 派单 | `spawn_agent` | 接到新的合法 agent_id 且真实状态正常；有写入优先 `git_isolation=required`（若可用），超时/副作用界限明确 |
| 回收 | `wait_agents`, `get_agent(full)` | 区分wait超时与执行器失败，核实真实结果、model、native session、worktree状态 |
| 请示/继续 | `agent_action(message)` | 同原生session继续且上下文答复正确；需校验parent和权限 |
| 合并 | `agent_action(apply)` | 源工作区diff、测试独立通过，官方apply回执确认；冲突即停，不自动reset/clean |
| 留存 | `scripts/checkpoint.py` | note、绑定会话、snapshot、verify全部记录，权限不由文件代替 |

**重要**：官方 `admission_token_budget` 是任务接纳阈值，不是已经运行任务的严格硬费用上限；provider用量缺失时记录UNKNOWN。Codex/Work额度与 Chat额度不是简单相加的无限次数。
