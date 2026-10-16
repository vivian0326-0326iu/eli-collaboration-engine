# 发布候选本地验收记录（2026-10-16）

**已在当前工作容器内真实完成**（并非全新 Mac 或真实陌生 ChatGPT 账号）：

- `python3 -m unittest discover -s tests -v`：**10 项本地单元测试全部通过**，测试任务登记、Git 快照校验、错误停止、session 不匹配与请示决策。
- `scripts/install_local.sh`：在新建的临时 Git 仓库首次运行成功，复制模板、Skill、进度脚本和部署文档；第二次调用确实拒绝覆盖已有文件；初始化、note、snapshot、verify 全部通过。
- `examples/bug-demo`：故意保留 1 个失败测试（`add(-2,3)` 被错误实现成 5 而非1）；用于以后让 Codex 真正修复，**不算公开包自身验证失败**。
- `scripts/audit_release.py`：扫描文本文件中明显的私有 Mac 路径/令牌模式，0 个模式命中。**启发式扫描不等于绝对安全审计**。
- ZIP 内文件完整性核验通过，包含 `README.md`、正式 Skill、主控指令、安装/验收/恢复/发布指南、MIT LICENSE、测试代码。

**尚无独立真实验收**：一套完全空白的真实 Mac + 陌生用户账号，从初次安装 Mac MCP/Codex 到 ChatGPT 自定义 MCP 插件真实连接、A-H 全流程完成。某些账号不可用写权限时会 BLOCKED，文档不能绕过。

作者私有项目 `108/108` 是另一套历史测试，不是该发布候选成绩。不要偷换。
