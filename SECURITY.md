# 安全、隐私与默认权限

本仓库是运行在用户自己的 Mac 和 ChatGPT 账号上的**协作设置与辅助工具**，不是对用户电脑的远程托管。只按官方允许的权限使用，不提供绕过 ChatGPT 账号工具限制的办法。

## 不应该发布或发送给其他人

- ChatGPT/ Codex 登录凭证、`auth.json`、API Key、MCP 服务密钥、ngrok tunnel token；
- 带认证参数的完整 `/mcp` URL、`~/.mac-mcp/settings.json` 或 `.env` 全文；
- 用户私有仓库、原始聊天、Mac 真正的用户名路径、私有 agent/session/workflow 标识；
- 用户本机 `.eli-engine/` 任务状态、被测试 Git worktree 中真实客户数据。

GitHub 公开仓库采用本包 `.gitignore` 排除 `.env*`、token、`.eli-engine/` 和字节码。**不要以为 `.gitignore` 是秘密扫描器**；任何手动添加或旧 Git 历史里的密钥还需要独立审计/撤销。

## Mac MCP/ChatGPT 权限

- 一开始先只读。要写入文件或运行命令，需明确允许特定仓库或练习目录。
- 如果 ChatGPT 账号没有可写入的自定义 MCP 权限，就不能用本包的一段 prompt 模拟拥有该权限。
- `trusted` 是 Mac MCP 更宽的授权档位，不等于单独的危险操作确认；Server Approval 是另一个独立安全开关。
- 如果必须远程 MCP 通道，优先官方安全隧道；自行维护公网 HTTPS 时必须开启认证、TLS 与 HostGuard，不能不经用户授权自动暴露 Mac 端口。
- 不通过 AppleScript、终端注入、浏览器 UI 自动操作 ChatGPT 自身以规避官方限制。
- 选择支持隔离 worktree 的 `workspace_write` 且 `git_isolation=required`，合并前主控必须独立审查。禁止 `git reset --hard`、`git clean -fd` 等无授权清理。

## 任务状态 ≠ 真实安全授权

`scripts/checkpoint.py` 的状态和摘要用于避免误用旧进度。它不验证远端签名、不强制拦截 Mac MCP `agent_action`，也不保证跨多个文件数据库事务。`bind/report/decide` 的结果须由主控通过真实 `get_agent` 核实，日志来源不是模型自己说成功就算成功。

## 发布检查

请参见 [`PUBLISHING_CHECKLIST.md`](PUBLISHING_CHECKLIST.md)。如果发现漏洞，请使用 GitHub Issue **只发布脱敏复现**，不要贴明文秘钥。涉及可利用漏洞时，优先联系对应上游开发者的私人安全通道。
