# 真实闭环的安全练习项目

这个示例 **故意留了一个小 Bug**：`add(-2,3)` 当前错误返回 5，正确结果应为 1。它不连接网络、不读取用户文件，也不涉及账号或密钥。

先进入 `examples/bug-demo` 运行：

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

预期：1 个测试失败。随后由普通 ChatGPT 主控调用已授权 Mac MCP 的 Codex 在隔离工作区修复 `mini_calc.py`，让 `test_negative` 通过。主控独立检查 diff、合并和再运行测试，然后记录任务与 Git 检查点。

**这项离线练习只能测代码和测试。** 若要宣称双向真实协作完成，必须有实际 Mac MCP `spawn_agent/wait_agents/get_agent/agent_action(message)` 以及 session ID 一致的回执。不要用运行这套本地测试冒充连接通过。
