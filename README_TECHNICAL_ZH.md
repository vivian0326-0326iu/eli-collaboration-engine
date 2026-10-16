# eli｜协作引擎 · 从零搭建版

**让你平时使用的普通 ChatGPT 负责思考、指挥和验收，让 Codex 真正执行代码任务；遇到问题双方直接往返，而不是让人类充当复制粘贴员。**

![status](https://img.shields.io/badge/release-source--preview-blue) ![python](https://img.shields.io/badge/Python-3.10%2B-blue) ![platform](https://img.shields.io/badge/platform-macOS-lightgrey) ![license](https://img.shields.io/badge/license-MIT-lightgrey)

> **先说重点：这是一份能真正按步骤搭建的开源仓库，而不是一条万能提示词。** 其中的文件、Skill、本地管理脚本和测试可以直接运行；但 Mac MCP、Codex、ChatGPT 插件由各自的产品提供。**没有相应账户权限、Mac 授权或网络认证，任何 AI 都不能凭这份 README 凭空获得电脑控制能力。**
>
> **验收口径**：本仓库的本地 Python 测试已实际运行；原作者私有环境曾完成 ChatGPT→Mac MCP→Codex 原生会话双向返工、隔离代码修复和 Git 提交（当时私有库108项回归PASS）。**本公开包尚未在陌生用户的全新 ChatGPT 账户+全新 Mac 上完成端到端冷启动验收**。读者必须按文档自己做 A-H 真实验收，不能把作者通过的结果写成你的 PASS。

## 一分钟看懂

```text
旧方式：你问ChatGPT → 复制给Work → Work报错 → 复制回Chat → Chat给新方案 → 再转发...

新方式（以本地权限真实可用为前提）：
你 → 普通ChatGPT主控（复杂判断/决定/验收）
                 ⇅ 已授权 Mac MCP 官方工具
            Codex 原生执行器（读文件/修Bug/跑测试）
                 ⇅ 同一可恢复的 Codex provider-native session
         Git隔离修改、真实工具结果、本地项目进度
```

**和“自动唤醒旧云 Work”不是一回事**：本仓库搭建的是普通 Chat 与 Codex 原生代理的双向协作。它**不能**向你过去的某条 ChatGPT 云 Work 线程直接发消息，也不能保证关掉聊天后主控仍 24×7 工作。

## 先选择你的情况

**情况 A：你完全没有配置过。** 打开 [从零安装](docs/01-从零安装.md)。先确认账号是否有可写入的自定义 MCP 能力、Mac MCP 安装条件和自己的 Codex 账号。完成后再给 ChatGPT [这份完整启动任务书](prompts/00-交给毛坯ChatGPT.md)。

**情况 B：你有 Mac MCP、Codex、ChatGPT 已连接工具。** 先跑 `python3 scripts/doctor.py --project .` 看本机能力，再按 [A-H真实验收](docs/02-真实接入与四关验收.md) 测试。不要因为提示词会回答“我可以”就认定全部通过。

**情况 C：你已经有一个 Git 项目，想让它采用这套协作习惯。** 把下面命令中的路径换成你已有的**可控 Git 项目路径**：

```bash
# 在本开源包根目录执行，目标项目已有 AGENTS.md 等文件时会拒绝覆盖
sh scripts/install_local.sh /path/to/your-git-project
```

然后确认目标项目 `.gitignore` 中有 `.eli-engine/`，审查新增文件、提交 Git，才在目标仓库执行：

```bash
python3 scripts/checkpoint.py init --name '我的项目'
python3 scripts/checkpoint.py note --done '协作规则已安装' --next '真实连接A-D测试'
python3 scripts/checkpoint.py snapshot --reason '干净项目初始检查点'
python3 scripts/checkpoint.py verify
```

## 5 步完整路径

1. **检查权限和环境**：[docs/01-从零安装.md](docs/01-从零安装.md) 包含 Mac/Git/Python/Codex CLI/Mac MCP/ChatGPT 自定义连接的上游文档和具体入口。**账号功能不可用时明确 BLOCKED**。
2. **主控身份**：把 [`templates/CHATGPT_CUSTOM_INSTRUCTIONS.md`](templates/CHATGPT_CUSTOM_INSTRUCTIONS.md) 放进 ChatGPT 全局自定义指令；若你在 ChatGPT Project 中使用，注意项目级指令可能覆盖全局规则。
3. **代理角色 + Skill**：Codex 在你的 Git 项目根目录读取 `AGENTS.md`，项目下 `.agents/skills/eli-collaboration-engine/SKILL.md` 是 Skill 发现入口。**Skill 不是 ChatGPT 插件，也不等于完整 Mac MCP**。
4. **真机验收 A-H**：[docs/02-真实接入与四关验收.md](docs/02-真实接入与四关验收.md) 从普通 Chat 的 A-D 文件四关开始，接着 Codex 真实派单、原生会话追问、隔离工作树实际 Bug 修复、主控验收和 Git 提交。
5. **留下可恢复状态**：[docs/03-双向协作与长期恢复.md](docs/03-双向协作与长期恢复.md)，使用本地 Python CLI 记录会话绑定、提问、决策、错误、Git SHA 和内容摘要；新 Chat 来时先读真实状态，不靠“记得”两个字。

完成所有实际关卡的**最小必需成果**是：在普通 Chat 里看见真正的 Mac MCP 连接、能通过它调用 Codex、真实 `agent_action(message)` 继续同一 Codex 原生会话、由 ChatGPT 独立验收一次修复、最终在你自己的 Git 目录里保留提交和恢复检查点。

## 本仓库里有哪些东西？

```text
eli-collaboration-engine/
├── README.md                         # 你现在看的首页
├── prompts/00-交给毛坯ChatGPT.md       # 可以复制给普通ChatGPT的“从零搭建任务书”
├── templates/
│   ├── CHATGPT_CUSTOM_INSTRUCTIONS.md  # 普通ChatGPT主控
│   ├── AGENTS.md                       # Codex执行器
│   ├── PROJECT_CONTEXT.md              # 每个项目填写自己的信息
│   └── WORKFLOW.md                     # 派单/请示/验收合同
├── .agents/skills/eli-collaboration-engine/
│   ├── SKILL.md                        # 真实 Codex Skill 入口
│   └── references/                     # 主控/工具合同
├── scripts/
│   ├── doctor.py                       # 只读本机准备检查（不看秘密）
│   ├── install_local.sh                # 只写到你指定的目标Git项目
│   └── checkpoint.py                   # 本地任务、决策、恢复及Git检查点
├── examples/bug-demo/                 # 故意有Bug的演练工程
├── tests/                              # 离线可重复的Python单元测试
├── docs/                               # 完整安装、接入、恢复和GitHub发布指南
├── SECURITY.md / LICENSE / SOURCES_AND_CLAIMS.md
└── PUBLISHING_CHECKLIST.md
```

本地检查（在本仓库根目录）：

```bash
python3 scripts/doctor.py --project .
python3 -m unittest discover -s tests -q
```

如果你使用 `examples/bug-demo/`，它的 `test_negative` 本来就应该先失败，用来测试真正的 AI 修复；**不要把该演示预置失败混入本仓库主测试套件**。

## 关于省额度

这个项目的价值是**把昂贵的判断和高频可验收的执行分开**，减少重复上下文搬运。Chat 使用额度与 Work/Codex 工作额度有不同口径，Work 与 Codex 有共享额度安排；不同账号、模型、地区与任务长度差异很大。我们没有通过配对实验得出固定节省百分比，也不保证任何模型免费无限调用。官方额度以你自己的当下账户显示为准，缺失记作 UNKNOWN。详情见 [SOURCES_AND_CLAIMS.md](SOURCES_AND_CLAIMS.md)。

## 关心 GitHub 怎么发？

大多数“开源 Skill”博主不是发布一个神秘安装软件，而是**公开 GitHub 仓库 + `README.md` + `SKILL.md` + 文件与脚本 + Release ZIP**。GitHub 打开仓库就能看到 README；Codex 等支持 Skills 的工具根据目录和元数据发现 Skill。我们的包已经按这种格式整理好。**不会因为放上 GitHub 就让陌生账号自动拥有 Mac MCP 权限。**

从零发布步骤见 [docs/04-GitHub如何发布.md](docs/04-GitHub如何发布.md)。本次交付是**本地可下载发布候选**，**尚未上传 GitHub 或替你公开分享**。

## 安全与授权

不上传用户私密的 `~/.codex/`、`~/.mac-mcp/`、ChatGPT 聊天原文、API Key、真实隧道凭据。Mac MCP 的 `trusted` 是高权限，不等于所有操作有额外确认。开启公网只在用户认可安全边界后进行。写入任务优先 `git_isolation=required`，失败时不可暴力回放。详细见 [SECURITY.md](SECURITY.md)。

**依赖与署名**：这是独立的配置、协作协议和本地辅助代码，**不包含 Mac MCP 或 Codex 的第三方源码**；它们分别由原作者维护。示例原创文件按本仓库 MIT 许可使用。
