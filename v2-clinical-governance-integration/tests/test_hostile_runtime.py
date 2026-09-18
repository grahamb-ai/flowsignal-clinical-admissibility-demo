import copy, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from ambient_runtime import *
from test_ambient_runtime import attempt, conditions

class HostileTests(unittest.TestCase):
    def test_tampered_receipt_blocked(self):
        a=attempt(); r=evaluate(a,conditions()); r["decision"]="ALLOW"; r["attempt"]["patient_id"]="victim"
        self.assertEqual("RECEIPT_INTEGRITY_FAILED",execute(r,a,conditions())["reason_code"])

    def test_fail_open_not_permitted_when_clinician_disappears(self):
        a=attempt(); r=evaluate(a,conditions(state_version=1))
        cur=conditions(clinician_present=False,state_version=2)
        self.assertEqual("BLOCKED",execute(r,a,cur)["status"])

    def test_coherent_rollback_old_state_version_cannot_reuse_receipt(self):
        a=attempt(); r=evaluate(a,conditions(state_version=7))
        # attacker presents otherwise-valid earlier-looking state
        rolled=conditions(state_version=6)
        self.assertEqual("AUTHORITY_STATE_STALE_REEVALUATION_REQUIRED",execute(r,a,rolled)["reason_code"])

    def test_duplicate_exact_execution_is_not_yet_prevented(self):
        # Same challenge after remediation: second use of the same receipt must fail.
        a=attempt(); c=conditions(); r=evaluate(a,c); gateway=ExecutionGateway()
        first=gateway.execute(r,a,c); second=gateway.execute(r,a,c)
        self.assertEqual("EPR_COMMIT_PERMITTED",first["status"])
        self.assertEqual(("BLOCKED","AUTHORITY_RECEIPT_ALREADY_CONSUMED"),
                         (second["status"],second["reason_code"]))

if __name__=="__main__": unittest.main()
