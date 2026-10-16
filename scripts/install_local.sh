#!/bin/sh
# Only adds files inside the USER-SELECTED local Git project, never Mac MCP or account settings.
set -eu
if [ "$#" -ne 1 ]; then
  printf '%s\n' '用法: sh scripts/install_local.sh /path/to/your-existing-git-project' >&2
  exit 2
fi
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
KIT_ROOT=$(dirname -- "$SCRIPT_DIR")
TARGET=$1
[ -d "$TARGET" ] || { echo '目标目录不存在' >&2; exit 2; }
TARGET=$(CDPATH= cd -- "$TARGET" && pwd)
git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo '目标不是Git仓库' >&2; exit 2; }
[ -f "$TARGET/AGENTS.md" ] && { echo '目标已有 AGENTS.md；拒绝覆盖，请手动合并' >&2; exit 3; }
[ -e "$TARGET/scripts/checkpoint.py" ] && { echo '目标已有 scripts/checkpoint.py；拒绝覆盖' >&2; exit 3; }
[ -e "$TARGET/.agents/skills/eli-collaboration-engine" ] && { echo '目标已有同名 Skill；拒绝覆盖' >&2; exit 3; }
[ -e "$TARGET/docs/eli-engine" ] && { echo '目标已有 docs/eli-engine；拒绝覆盖' >&2; exit 3; }
mkdir -p "$TARGET/scripts" "$TARGET/.agents/skills" "$TARGET/docs/eli-engine"
cp "$KIT_ROOT/templates/AGENTS.md" "$TARGET/AGENTS.md"
cp "$KIT_ROOT/scripts/checkpoint.py" "$TARGET/scripts/checkpoint.py"
cp "$KIT_ROOT/scripts/doctor.py" "$TARGET/scripts/doctor.py"
cp "$KIT_ROOT/templates/WORKFLOW.md" "$TARGET/docs/eli-engine/WORKFLOW.md"
cp "$KIT_ROOT/templates/PROJECT_CONTEXT.md" "$TARGET/docs/eli-engine/PROJECT_CONTEXT.md"
cp "$KIT_ROOT/docs/03-双向协作与长期恢复.md" "$TARGET/docs/eli-engine/03-双向协作与长期恢复.md"
cp -R "$KIT_ROOT/.agents/skills/eli-collaboration-engine" "$TARGET/.agents/skills/eli-collaboration-engine"
printf '%s\n' '✅ 本地模板已复制。未安装Mac MCP，未连接公网，未更改账号权限，也未调用模型。'
printf '%s\n' '请手动确保 .gitignore 忽略 .eli-engine/；确认以上文件后提交一次Git，再 init / snapshot。'
