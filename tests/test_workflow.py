"""Offline workflow state tests. These do not touch Mac MCP or a model."""
import json
import io
import contextlib
import importlib.util
import types
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CLI = BASE / 'scripts/checkpoint.py'
DOCTOR = BASE / 'scripts/doctor.py'
_spec = importlib.util.spec_from_file_location('eli_public_checkpoint', CLI)
_checkpoint = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_checkpoint)

class WorkflowStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for params in [('init','-q'),('config','user.email','test@example.invalid'),('config','user.name','Test Runner')]:
            subprocess.run(['git',*params],cwd=self.root,check=True,capture_output=True)
        (self.root/'.gitignore').write_text('.eli-engine/\n')
        subprocess.run(['git','add','.gitignore'],cwd=self.root,check=True,capture_output=True)
        subprocess.run(['git','commit','-qm','initial'],cwd=self.root,check=True,capture_output=True)
        self.cli('init','--name','demo')
    def cli(self,*cmd,ok=True):
        out = io.StringIO()
        err = io.StringIO()
        status = 0
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                status = _checkpoint.main(['--root', str(self.root), *cmd, *(['--workspace', str(self.root)] if cmd[0] == 'init' else [])])
        except (_checkpoint.StateError, OSError) as exc:
            status = 3
            err.write('ERROR: '+str(exc))
        x = types.SimpleNamespace(returncode=status,stdout=out.getvalue(),stderr=err.getvalue())
        self.assertEqual(x.returncode == 0,ok,(cmd,x.stdout,x.stderr))
        return x
    def test_bind_and_read_only_resume_candidate(self):
        self.cli('bind','--provider','codex','--agent-id','agt_abcdef0011','--session-id','session_abcd123456')
        self.cli('note','--done','A-D','--next','retry scenario')
        self.assertIn('STOP_REVIEW',self.cli('plan',ok=False).stderr)
        self.cli('snapshot','--reason','verified')
        self.assertIn('VERIFY_AGENT_LIVE_FIRST',self.cli('plan').stdout)
    def test_needs_controller_decision_and_duplicate_guard(self):
        self.cli('bind','--provider','codex','--agent-id','agt_abcdef0011','--session-id','session_abcd123456')
        self.cli('report','--agent-id','agt_abcdef0022','--session-id','session_abcd123456',
                 '--outcome','needs_controller','--summary','Fix style A or B?')
        self.assertIn('WAITING_CONTROLLER',self.cli('plan',ok=False).stderr)
        self.cli('decide','--answer','Choose A')
        self.cli('snapshot','--reason','controller accepted')
        self.assertIn('VERIFY_AGENT_LIVE_FIRST',self.cli('plan').stdout)
        self.assertIn('NEW result agent',self.cli('report','--agent-id','agt_abcdef0022','--session-id','session_abcd123456',
                                         '--outcome','completed','--summary','again',ok=False).stderr)
    def test_failed_agent_stops_replay(self):
        self.cli('bind','--provider','codex','--agent-id','agt_abcdef0011','--session-id','session_abcd123456')
        self.cli('report','--agent-id','agt_abcdef0022','--session-id','session_abcd123456',
                 '--outcome','timeout','--summary','unknown side effect')
        self.cli('snapshot','--reason','failure forensic')
        self.assertIn('STOP_REVIEW',self.cli('plan',ok=False).stderr)
        self.assertIn('independent recovery', self.cli('bind','--provider','codex',
                       '--agent-id','agt_abcdef0033','--session-id','session_abcd123456',ok=False).stderr)
    def test_mismatch_never_accepted(self):
        self.cli('bind','--provider','codex','--agent-id','agt_abcdef0011','--session-id','session_abcd123456')
        self.assertIn('mismatch',self.cli('report','--agent-id','agt_abcdef0022','--session-id','different000000',
                                         '--outcome','completed','--summary','test',ok=False).stderr)
        self.assertIn('independent',self.cli('bind','--provider','codex','--agent-id','agt_abcdef0033',
                                            '--session-id','new_session9999',ok=False).stderr)
    def test_doctor_does_not_claim_connected(self):
        p = subprocess.run([sys.executable,str(DOCTOR),'--project',str(self.root)],capture_output=True,
                           text=True,timeout=8,check=True)
        obj = json.loads(p.stdout.split('Local CLI presence')[0].split('NOTICE:')[0])
        self.assertEqual(obj['chatgpt_mcp_plugin_available'],'NOT_VERIFIABLE_FROM_LOCAL_SHELL')
        self.assertFalse(obj['external_model_calls'])

if __name__ == '__main__': unittest.main()
