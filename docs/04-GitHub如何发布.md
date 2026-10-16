# 给没用过 GitHub 的人：怎么发布开源 Skill / AI 项目？

## 博主通常在 GitHub 发的是什么？

其实就是一个**公开文件夹（Repository，仓库）**：
- `README.md` 是首页说明，GitHub 会自动展示；
- `.agents/skills/…/SKILL.md` 是 Codex 可识别的 Skill 元数据和流程，**只在支持的工具中生效**；
- `AGENTS.md` 写给 Codex 的工作规则，不等于 ChatGPT 的自定义指令；
- `scripts/` 是真正能运行的辅助工具，不是纯文字；
- `tests/` 是自动化测试；
- `docs/` 是详细图文或排障；
- `LICENSE` 决定其他人是否可以复制修改；
- GitHub 的 **Releases** 可再附 ZIP，方便小红书读者下载。

**推荐形式**：公开 GitHub 仓库 + 原生 Skill 文件夹 + 完整 README + 安装/验收脚本，而不是只发布一段提示词。官方 Codex Skill 结构参考 https://developers.openai.com/codex/skills 。

## 不会命令行的发布办法（GitHub Desktop）

1. 注册/登录 GitHub。先把本 ZIP 下载并解压到**一个不包含私人配置的文件夹**。
2. 建议用项目名 `eli-collaboration-engine`，描述 `ChatGPT controller + Mac MCP + Codex, with verifiable handoff and recovery`。
3. 下载 GitHub Desktop（github.com/apps/desktop）；File → Add local repository。如果还不是 Git 仓库，可 File → New repository，选择解压后的目录或将文件导入其中。
4. **发布前先扫一遍**：不能包含个人 Mac 路径、真实 API Key、ngrok token、公网隧道账号、私人原始聊天、agent/session内部标识、`.eli-engine/`、`~/.mac-mcp/` 或 `~/.codex/` 下的配置。
5. GitHub Desktop 查看 Changes，只提交本包公开文件；点击 `Commit to main`。
6. 点击 `Publish repository`，**明确检查是否选择 `Keep this code private`**：如果要开源就公开；不确定先私有，审计好再切 Public。
7. 在网页打开你的仓库，确认 README 头部正常，`.agents/skills/eli-collaboration-engine/SKILL.md` 可以点击查看，`LICENSE` 显示，所有文件都是公开模板。
8. 需要一键 ZIP 下载时，读者可以点 **Code → Download ZIP**。若要单独版本发布，仓库右侧 **Releases → Draft a new release**，tag 如 `v1.0.0`，写真实 release notes，然后附 ZIP。

## 熟悉终端时

```bash
cd /path/to/eli-collaboration-engine
# 检查无私人数据再初始化本地仓库
git init
git add .
git commit -m 'Initial public release'
# 在GitHub创建空仓库，使用网站提供的真实URL，不要照抄示例
# git remote add origin https://github.com/<你的账号>/<你的仓库>.git
# git push -u origin main
```

若已用 GitHub Desktop 发布，就不必再重复用命令行初始化仓库。

## GitHub 仓库的“Use this template”有什么用？

在仓库 Settings → General 找到 **Template repository**（界面可能变化）。启用后，访客可以用 **Use this template** 创建自己的仓库副本，而不仅仅 Fork 你的原项目。这特别适合 AI 协作配置模板。

## 关于开源许可和署名

本包原创教程和本地辅助脚本采用 MIT 示例许可。**Mac MCP、Codex、ChatGPT 都由各自项目维护，不能把别人产品的源码打包伪装成自己原创，也不能发布登录令牌或私有配置。**

有关创建仓库和 Release 的官方步骤：
- https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories
- https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

**本交付没有替用户创建公开 GitHub 仓库，公开发布仍需用户确认**。先上传私人历史项目的源仓库十分危险，请只使用这一份已经脱敏的公开目录。
