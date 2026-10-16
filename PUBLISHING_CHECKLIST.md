# 开源发布前的最后确认

**发布动作还没有执行。** 这是一份用于作者在 GitHub 公开前的核对表，不应由 AI 未经授权直接创建公共仓库。

- [ ] 公开源码不包含私人 Mac 绝对路径、邮箱、密码、API Key、ngrok 账号、ChatGPT agent/session/workflow ID 或私人对话。
- [ ] 仅发布本目录（独立重新编写的公开模板），不要把作者的私有工程 `~/.codex` / `~/.mac-mcp` 整个提交。
- [ ] 在本目录运行 `python3 -m unittest discover -s tests -q` 并记录**本公开包**测试数量。**108项是原私有工程的历史测试数，不是本仓库测试数。**
- [ ] `examples/bug-demo` 故意有 Bug，要在说明里指出预期失败，不能宣传公开包所有可能测试都无误。
- [ ] GitHub 首页 README 与教程可以一一点击、Skill 路径 `.agents/skills/eli-collaboration-engine/SKILL.md` 完整。
- [ ] 官方依赖、账户权限与模型可用性被明确说明；不能说“毛坯 ChatGPT 复制提示词就一键安装成功”。
- [ ] 通过一个**新的测试项目**执行 A-D、Codex 派单、同一 native session 追问、实际代码修复和 Git/状态保存，并记录真实证据。
- [ ] 另找一套**从未安装过**的 Mac/ChatGPT 账户完成冷启动端到端 A-H；如果没做，Release 明确标 `未进行陌生环境独立验收`。
- [ ] 用 GitHub Desktop 或 CLI 提交后，再次浏览 GitHub 公开页面逐一检查可见内容及忽略列表。
- [ ] 发布 ZIP 之前确认没有真实 token 和 `.eli-engine/` 私有进度。
- [ ] 每次发布说明实际改动、验证范围和不兼容项，不用作者私人测试数冒充本次运行数据。
