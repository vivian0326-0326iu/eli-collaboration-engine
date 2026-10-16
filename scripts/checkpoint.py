#!/usr/bin/env python3
"""Small LOCAL progress register for eli Collaboration Engine.

Does not dispatch models, contact ChatGPT, call Mac MCP, or enforce external
permissions. State files are private, ignored by Git, and fail closed on drift.
Requires Python 3.10+ and macOS/POSIX fcntl locking.
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

BJ = timezone(timedelta(hours=8))
MAX_EVENTS = 200
MAX_CONSULT_ROUNDS = 2
MAX_RESUME_ROUNDS = 3


class StateError(Exception):
    pass


def now():
    return datetime.now(BJ).isoformat(timespec="seconds")


def validate_line(value: str, label: str, max_len: int = 1500) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > max_len:
        raise StateError(f"{label} must be nonempty (<= {max_len} chars)")
    if any(ord(c) < 32 and c not in "\n\t" for c in value):
        raise StateError(f"{label} contains control characters")
    return value.strip()


def git(root: Path, *args: str) -> str:
    try:
        proc = subprocess.run(["git", "-C", str(root), *args],
                              capture_output=True, text=True, timeout=8,
                              check=False)
    except (OSError, subprocess.TimeoutExpired) as err:
        raise StateError(f"git is unavailable: {type(err).__name__}") from err
    if proc.returncode:
        raise StateError(f"git {' '.join(args)} failed (status {proc.returncode})")
    return proc.stdout.strip()


def git_proof(root: Path) -> str:
    head = git(root, "rev-parse", "--verify", "HEAD").lower()
    if not re.fullmatch(r"[a-f0-9]{40,64}", head):
        raise StateError("invalid Git HEAD")
    if git(root, "status", "--porcelain=v1", "--untracked-files=normal"):
        raise StateError("Git working tree is dirty; review and commit first")
    return head


def fingerprint(record: dict) -> str:
    # Exclude snapshots to avoid circular dependency.
    x = {k: v for k, v in record.items() if k != "snapshots"}
    data = json.dumps(x, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _state_file(root: Path) -> Path:
    return root / ".eli-engine" / "state.json"


def load(root: Path) -> dict:
    path = _state_file(root)
    if path.is_symlink():
        raise StateError("refusing symlinked state file")
    if not path.exists():
        raise StateError("no project state; run init first")
    if path.stat().st_size > 512_000:
        raise StateError("state too large for bounded local reader")
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise StateError(f"invalid local state: {type(exc).__name__}") from exc
    if (not isinstance(obj, dict) or obj.get("schema") != 1
            or obj.get("workspace") != str(root)
            or not isinstance(obj.get("snapshots"), list)
            or not isinstance(obj.get("events"), list)
            or len(obj["events"]) > MAX_EVENTS):
        raise StateError("invalid or relocated project state")
    return obj


def save(root: Path, obj: dict):
    folder = root / ".eli-engine"
    if folder.is_symlink():
        raise StateError("refusing symlinked state directory")
    folder.mkdir(mode=0o700, exist_ok=True)
    if not folder.is_dir():
        raise StateError("invalid state directory")
    os.chmod(folder, 0o700)
    old = _state_file(root)
    if old.is_symlink():
        raise StateError("refusing symlinked state file")
    fd, temp = tempfile.mkstemp(prefix=".state-", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            os.chmod(temp, 0o600)
            json.dump(obj, out, ensure_ascii=False, indent=2, sort_keys=True)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
        os.replace(temp, old)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


@contextlib.contextmanager
def locked(root: Path):
    d = root / ".eli-engine"
    if d.is_symlink():
        raise StateError("refusing symlinked state directory")
    d.mkdir(mode=0o700, exist_ok=True)
    lp = d / ".write.lock"
    if lp.is_symlink():
        raise StateError("refusing symlinked lock")
    fd = os.open(str(lp), os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        with os.fdopen(fd, "r+") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            yield
    finally:
        # fcntl lock automatically released on descriptor close.
        pass


def main(argv=None):
    ap = argparse.ArgumentParser(description="eli collaboration: local progress only; NO model calls")
    ap.add_argument("--root", default=".", help="project root (default current directory)")
    subs = ap.add_subparsers(dest="command", required=True)
    p = subs.add_parser("init")
    p.add_argument("--workspace", default=".")
    p.add_argument("--name", required=True)
    subs.add_parser("show")
    p = subs.add_parser("note")
    p.add_argument("--done", required=True)
    p.add_argument("--next", required=True)
    p.add_argument("--status", choices=["active", "blocked", "completed"], default="active")
    p = subs.add_parser("snapshot")
    p.add_argument("--reason", required=True)
    subs.add_parser("verify")
    p = subs.add_parser("bind")
    p.add_argument("--provider", choices=["codex"], required=True)
    p.add_argument("--agent-id", required=True)
    p.add_argument("--session-id", required=True)
    p.add_argument("--workflow-id", default="")
    p = subs.add_parser("report")
    p.add_argument("--agent-id", required=True)
    p.add_argument("--session-id", required=True)
    p.add_argument("--outcome", choices=["completed", "needs_controller", "failed", "timeout"], required=True)
    p.add_argument("--summary", required=True)
    p = subs.add_parser("decide")
    p.add_argument("--answer", required=True)
    subs.add_parser("plan")
    a = ap.parse_args(argv)
    root = Path(a.root).expanduser().resolve()
    if not root.is_dir():
        raise StateError("project root is not a directory")
    if a.command == "init":
        workspace = Path(a.workspace).expanduser().resolve()
        if workspace != root:
            raise StateError("workspace must equal --root (or launch CLI from workspace)")
        name = validate_line(a.name, "name", 120)
        with locked(root):
            if _state_file(root).exists() or _state_file(root).is_symlink():
                raise StateError("refusing to overwrite existing project state")
            record = dict(schema=1, project=name, workspace=str(root),
                          status="active", done="Initialized local state",
                          next="Verify Mac MCP capabilities and A-D smoke tests",
                          updated_bjt=now(), events=[], snapshots=[],
                          agent=None, consult_rounds=0, resume_rounds=0,
                          pending_question=None, last_agent_outcome=None)
            save(root, record)
        print("INITIALIZED local project state (no AI dispatched)")
        return 0
    if a.command == "show":
        record = load(root)
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return 0
    if a.command == "verify":
        record = load(root)
        if not record["snapshots"]:
            raise StateError("no snapshot saved")
        last = record["snapshots"][-1]
        if last.get("task_digest") != fingerprint(record):
            raise StateError("state changed since snapshot")
        if last.get("git_head") != git_proof(root):
            raise StateError("Git HEAD changed since snapshot")
        print("VERIFIED: local task digest + clean Git HEAD match last snapshot")
        return 0
    if a.command == "plan":
        record = load(root)
        if not record.get("agent"):
            raise StateError("NOT_READY: no bound, independently verified agent")
        if record["status"] == "waiting_controller":
            raise StateError("WAITING_CONTROLLER: review agent question and record decision")
        if record["status"] != "active":
            raise StateError("STOP_REVIEW: project not active")
        if record.get("consult_rounds", 0) > MAX_CONSULT_ROUNDS or record.get("resume_rounds", 0) >= MAX_RESUME_ROUNDS:
            raise StateError("BUDGET_STOP: manual review required")
        if record.get("last_agent_outcome") in {"failed", "timeout"}:
            raise StateError("STOP_REVIEW: unknown side effect; do not retry")
        if not record["snapshots"]:
            raise StateError("STOP_REVIEW: save independently verified checkpoint first")
        last = record["snapshots"][-1]
        if last.get("task_digest") != fingerprint(record) or last.get("git_head") != git_proof(root):
            raise StateError("STOP_REVIEW: Git or task state differs from checkpoint")
        latest = load(root)
        if fingerprint(latest) != fingerprint(record):
            raise StateError("STOP_REVIEW: task changed while reading")
        print(json.dumps({"action": "VERIFY_AGENT_LIVE_FIRST",
                          "note": "Not a server permission or dispatch receipt",
                          "agent": record["agent"], "done": record["done"],
                          "next": record["next"], "git_head": last["git_head"]},
                         ensure_ascii=False, indent=2))
        return 0
    with locked(root):
        record = load(root)
        if a.command == "bind":
            if record["status"] != "active" or record.get("last_agent_outcome") in {"failed", "timeout"}:
                raise StateError("STOP_REVIEW: blocked or failed project needs independent recovery; do not rebind in place")
            if not re.fullmatch(r"agt_[0-9a-zA-Z_-]{6,64}", a.agent_id):
                raise StateError("invalid Mac MCP agent ID")
            if not re.fullmatch(r"[0-9a-zA-Z_.:-]{8,160}", a.session_id):
                raise StateError("invalid provider native session ID")
            if record.get("agent") and record["agent"]["session_id"] != a.session_id:
                raise StateError("new native session needs independent recovery review; no silent overwrite")
            record["agent"] = {"provider": a.provider, "agent_id": a.agent_id,
                               "session_id": a.session_id, "workflow_id": a.workflow_id,
                               "source": "manually_transcribed_from_get_agent_not_authorization"}
            record["last_agent_outcome"] = None
            record["updated_bjt"] = now()
            save(root, record)
            print("BOUND agent metadata (must still verify live Mac MCP access)")
        elif a.command == "report":
            agent = record.get("agent")
            if not agent or a.session_id != agent["session_id"]:
                raise StateError("session mismatch; report not accepted")
            if a.agent_id == agent["agent_id"]:
                raise StateError("report requires a NEW result agent ID; do not re-ingest bound agent")
            if not re.fullmatch(r"agt_[0-9a-zA-Z_-]{6,64}", a.agent_id):
                raise StateError("invalid result agent ID")
            if any(e.get("result_agent_id") == a.agent_id for e in record["events"]):
                raise StateError("duplicate result agent ID")
            if record["status"] != "active":
                raise StateError("project not active; cannot ingest result")
            if len(record["events"]) >= MAX_EVENTS:
                raise StateError("history full")
            summary = validate_line(a.summary, "summary", 1000)
            if a.outcome == "needs_controller":
                record["consult_rounds"] = record.get("consult_rounds", 0) + 1
                record["status"] = "waiting_controller"
                record["pending_question"] = summary
            elif a.outcome in {"failed", "timeout"}:
                record["status"] = "blocked"
            record["last_agent_outcome"] = a.outcome
            record["agent"]["agent_id"] = a.agent_id
            record["updated_bjt"] = now()
            record["events"].append({"at_bjt": now(), "outcome": a.outcome,
                                     "result_agent_id": a.agent_id,
                                     "summary": summary, "provenance": "manual_transcription_not_signed_receipt"})
            save(root, record)
            print("SAVED agent result; verified live access and new snapshot required for more dispatch")
        elif a.command == "decide":
            if record["status"] != "waiting_controller" or not record.get("pending_question"):
                raise StateError("no pending controller question")
            if record.get("consult_rounds", 0) > MAX_CONSULT_ROUNDS or record.get("resume_rounds", 0) >= MAX_RESUME_ROUNDS:
                raise StateError("BUDGET_STOP: manual review/archival required")
            answer = validate_line(a.answer, "answer", 700)
            record["resume_rounds"] = record.get("resume_rounds", 0) + 1
            record["status"] = "active"
            record["pending_question"] = None
            record["last_agent_outcome"] = None
            record["updated_bjt"] = now()
            record["events"].append({"at_bjt": now(), "decision": answer,
                                     "reason": "controller-confirmed-not-automated"})
            save(root, record)
            print("DECISION saved; snapshot + get_agent verification before next message")
        elif a.command == "note":
            if record["status"] == "completed":
                raise StateError("completed record cannot be silently reactivated")
            if len(record["events"]) >= MAX_EVENTS:
                raise StateError("history full; archive after review")
            done = validate_line(a.done, "done")
            nxt = validate_line(a.next, "next")
            record.update(status=a.status, done=done, next=nxt, updated_bjt=now())
            record["events"].append({"at_bjt": now(), "status": a.status,
                                     "done": done, "next": nxt})
            save(root, record)
            print("SAVED local progress; snapshot still required after any changes")
        elif a.command == "snapshot":
            reason = validate_line(a.reason, "reason", 240)
            if len(record["snapshots"]) >= 200:
                raise StateError("snapshot history full; archive after review")
            head = git_proof(root)
            digest = fingerprint(record)
            # Recheck immediately before saving. Not a cross-file/dispatch lock.
            if git_proof(root) != head or fingerprint(load(root)) != digest:
                raise StateError("Git or state changed during snapshot")
            record["snapshots"].append({"at_bjt": now(), "reason": reason,
                                        "git_head": head, "task_digest": digest})
            save(root, record)
            print("SNAPSHOT saved: " + head[:12])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (StateError, OSError) as err:
        print("ERROR: " + str(err), file=sys.stderr)
        sys.exit(3)
