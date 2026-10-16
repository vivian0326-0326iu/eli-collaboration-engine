# eli｜协作引擎 · Chat + Codex 工作室

[English / README in English](README_EN.md) · [从零部署](docs/01-从零安装.md) · [完整技术手册](README_TECHNICAL_ZH.md) · [给 ChatGPT 的启动指令](prompts/00-交给毛坯ChatGPT.md) · [Codex Skill](.agents/skills/eli-collaboration-engine/SKILL.md)

> **不降智，少耗额度：整了个 Chat+Codex 工作室**
>
> 这不是无限免费、不是复制一段提示词就能接管电脑，也不是离线 24 小时自动工作。它是一套**在工具和账户权限允许时，普通 ChatGPT 与 Codex 可以实际双向协作**的开源工作流。

## 我为什么做这个项目？

故事开始于一个发现：我用普通 Chat 的高模型想方案，不会扣 Work/Codex 的工作额度。（普通 Chat 的额度，和 Work/Codex 的额度分开）

于是我让 Chat 负责规划，再把方案复制给 Work。结果日常变成：

Chat 出方案 → 我复制给 Work → Work 报错 → 我复制回 Chat → Chat 给新方案 → 我再复制过去。

两个 AI 都在干活，我成快递员了。😅🤖🤖

我就在想：能不能让擅长推理的 ChatGPT 做判断，让更适合高频执行的 Codex 动手？遇到问题，它们自己交流，不用我来回传话。

最后我搭出了「eli｜协作引擎」：

在ChatGPT 窗口里说“修一下这个 Bug”，它给 Codex 派单。Codex 遇到问题，把结果交回来；ChatGPT 重新判断，再把方案送回同一条 Codex 原生会话。

（做完还能检查代码、跑测试、提交 Git、保存进度。）

我们真实跑过一次完整流程：Codex 在隔离工作区改代码，ChatGPT 发现验收还差一步，就自己补上检查、合并提交。

不用反复复制粘贴，也有机会更合理地使用不同模型的额度。不过我没有做严格对比，不能说省了多少钱。（只是感觉我现在做轻量开发，基本上都没有走到 5 小时限额过）

（不是无限免费，不是 24 小时无人值守。是真实跑通的双向 AI 协作。纯小白不一定是最优解，欢迎讨论。）

我整理了可复刻的公开模板，包括 ChatGPT 主控指令、Codex 的 AGENTS.md、接入验收、返工流程和进度脚本。

## 30 秒看懂原理

```text
你 → 普通 ChatGPT（理解需求、判断、派单、验收）
                ↓ 已连接、已授权的 Mac MCP
           Codex 原生执行器（读取、编码、测试）
                ↓ 返回工具结果 / 遇阻请示
        ChatGPT 调整方案 → 继续同一可恢复会话
                ↓
           独立验收、Git 提交、本地检查点
```

这里的 **Codex 原生会话续接，不等于自动唤醒一条旧的云 Work 聊天**。如果 ChatGPT 的工具权限不足，也不能靠提示词强行连上 Mac。

## 从零复刻

**第一次使用：** 先阅读 [从零安装指南](docs/01-从零安装.md)，确认 macOS、Codex 登录、Mac MCP 与**当前 ChatGPT 账号能否实际调用自定义 MCP 工具**。然后使用 [完整启动任务书](prompts/00-交给毛坯ChatGPT.md)。

**安装到已有 Git 工程（在本仓库根目录执行）：**

```bash
sh scripts/install_local.sh /path/to/your-git-project
```

模板遇到已有同名文件会拒绝覆盖。随后参考 [真实接入 A–H 验收](docs/02-真实接入与四关验收.md)、[双向沟通与恢复](docs/03-双向协作与长期恢复.md)，检查本机环境：

```bash
python3 scripts/doctor.py --project .
python3 -m unittest discover -s tests -q
```

测试针对**本公开包的本地逻辑**，不是 ChatGPT ↔ Mac MCP 的联网联通测试。示例项目中故意留有 Bug，便于真实派单修复。

## 项目包含什么？

- [ChatGPT 主控指令](templates/CHATGPT_CUSTOM_INSTRUCTIONS.md) 与 [给空白 ChatGPT 的启动协议](prompts/00-交给毛坯ChatGPT.md)
- [Codex 的 AGENTS.md](templates/AGENTS.md)、[Skill](.agents/skills/eli-collaboration-engine/SKILL.md) 和 [工作流规则](templates/WORKFLOW.md)
- [部署指南](docs/01-从零安装.md)、[A–H 实测验收](docs/02-真实接入与四关验收.md)
- [本地进度工具](scripts/checkpoint.py)、[环境检查](scripts/doctor.py)、[回归测试](tests/)
- [安全说明](SECURITY.md)、[事实与宣传边界](SOURCES_AND_CLAIMS.md)、[MIT 许可证](LICENSE)

## 能力与成本的边界

普通 Chat 与 Work/Codex 的额度口径分开，但**额度、可用模型和自定义 MCP 能力会随账号、套餐及产品规则变化**。这里只介绍作者自己的工作方式，不保证每个人节省固定额度或金额，也不会把未知成本记成零。

作者私有系统曾完成真实双向交互和一次从 Codex 隔离代码修复到 ChatGPT 独立验收、Git 提交的工作闭环；**当时私有仓库 108 项测试通过**。这个数字不是公开包的测试数量，也不是新用户的端到端通过率。公开版**尚未完成陌生账号加全新 Mac 的独立冷启动验收**。

上游 Mac MCP 是独立开源项目：[bulutarkan/mac-mcp](https://github.com/bulutarkan/mac-mcp)。本仓库不包含 Mac MCP、Codex 或 ChatGPT 的私有组件，也不提供绕过产品权限的方法。

**License: MIT。** 欢迎交流复刻结果、真实限制、失败回执和改进方案。
