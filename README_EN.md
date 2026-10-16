# eli Collaboration Engine · Chat + Codex Studio

[简体中文 / 中文介绍](README.md) · [Setup guide (Chinese)](docs/01-从零安装.md) · [Technical guide (Chinese)](README_TECHNICAL_ZH.md) · [Controller prompt](prompts/00-交给毛坯ChatGPT.md) · [Codex Skill](.agents/skills/eli-collaboration-engine/SKILL.md)

> **Keep the reasoning quality, use your quota more wisely: I built a Chat + Codex studio.**

This is a workflow for **real two-way collaboration** between ordinary ChatGPT and a Codex agent through an authorized Mac MCP connection. It is **not** unlimited free usage, a one-prompt computer takeover, or an unattended 24/7 AI company.

## Why I built it

The story began when I realized that using a higher-capability model in ordinary ChatGPT to plan my next steps didn't use up my Work/Codex working quota. (Ordinary Chat usage and Work/Codex usage are tracked separately.)

So I used ChatGPT to plan and manually copied the plan into Work. My routine quickly became:

**ChatGPT suggests a plan → I paste it into Work → Work hits an error → I paste the error back → ChatGPT proposes a fix → I paste the fix into Work again.**

Two AIs were working. Somehow I became their delivery person. 😅🤖🤖

I wondered: why not let ChatGPT handle the harder decisions and verification, while Codex handles frequent execution? When Codex gets stuck, it should be able to report back; ChatGPT should decide what to try next and send the new instructions **into the same recoverable Codex-native session**, without me copying messages between windows.

That idea became **eli Collaboration Engine**.

Now, in my own tested setup, I can ask in an ordinary ChatGPT conversation: **"Please fix this bug."** ChatGPT delegates the task via Mac MCP. Codex investigates and edits code, returns results or blockers, and ChatGPT can re-evaluate and continue the native Codex session. The controller can also inspect diffs, run tests, commit to Git and save a project checkpoint.

This is more than a prompt demo. We tested a full, concrete cycle: Codex made a fix in an isolated worktree; ChatGPT noticed a missing verification step, completed it independently, applied the changes, and committed them.

The appeal is less copy-paste work and **potentially more efficient use of different model quotas**. I have not run a controlled cost comparison, so I cannot claim a fixed percentage or dollar amount saved. Anecdotally, for my lightweight projects I rarely reached the five-hour limit.

**Not unlimited free development. Not 24-hour unattended automation. Real two-way AI collaboration.** This may not be the easiest starting point for complete beginners; feedback and discussion are welcome.

I prepared reusable ChatGPT controller instructions, a Codex `AGENTS.md` template, setup checks, feedback-and-retry guidance and local project-state scripts.

## Architecture

```text
You → ordinary ChatGPT (reasoning, delegation, review)
              ↓ authorized Mac MCP tools
         Codex native agent (implementation, tests)
              ↓ reports and blockers
        ChatGPT decides → continue recoverable native session
              ↓
       independent verification, Git, checkpoint
```

**Important:** continuing a Codex-native agent session is **not** the same as waking an old ChatGPT cloud Work thread. The latter has not been implemented here. This system also requires an active conversation with the relevant tool permissions and does not run unattended after the conversation ends.

## Getting started

1. Read the [macOS installation guide (Chinese)](docs/01-从零安装.md). Verify eligibility for custom MCP tools in your **own** ChatGPT account, then install and authorize Codex and the upstream [Mac MCP](https://github.com/bulutarkan/mac-mcp) as appropriate.
2. Give your ChatGPT the [full setup instruction](prompts/00-交给毛坯ChatGPT.md), and use the [ChatGPT controller](templates/CHATGPT_CUSTOM_INSTRUCTIONS.md) and [Codex AGENTS.md](templates/AGENTS.md) templates.
3. Install the project template into **your own existing Git repo** by running the following in this repository's root:

```bash
sh scripts/install_local.sh /path/to/your-git-project
python3 scripts/doctor.py --project .
python3 -m unittest discover -s tests -q
```

4. Follow the [real connectivity and delegation checks (Chinese)](docs/02-真实接入与四关验收.md) and [session recovery guide (Chinese)](docs/03-双向协作与长期恢复.md). Treat unavailable permissions as blockers, not successful tests.

The local tests validate this public template's scripts only. They do not prove that a newly connected ChatGPT account can control Mac MCP. A small example intentionally contains a bug for an agent to fix during hands-on testing.

## What's in the repository?

Controller prompt, Codex Skill and `AGENTS.md`, installation instructions, a two-way feedback protocol, a local checkpoint utility, tests, a demo bug project, a safety guide and an MIT license. Detailed documents are currently primarily in Chinese; contributions and translations are welcome.

## Scope, evidence and limitations

The author's **private** system completed a real Codex-agent feedback loop and a code-delivery cycle; its original private repository had **108 passing unit tests at that time**. This is not a claim that the public template has 108 tests or that all new users will reproduce the full workflow without configuration.

**No independent end-to-end cold-start verification has yet been performed on a stranger's fresh Mac and ChatGPT account.** Features and quotas vary by plan and account; no fixed savings are claimed. This is an independent community workflow, not an official OpenAI product or a redistribution of Mac MCP or Codex.

See [Security](SECURITY.md), [Claims and source notes](SOURCES_AND_CLAIMS.md), and [MIT License](LICENSE).
