import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import ambient_runtime as runtime
from test_ambient_runtime import attempt, conditions

class AuthoritativeStateBoundaryHostileTests(unittest.TestCase):
    def test_missing_authoritative_state_fails_closed(self):
        a=attempt(); c=conditions(); r=runtime.evaluate(a,c)
        store=runtime.MemoryAuthorityStateStore()
        result=runtime.ExecutionGateway(state_provider=store).execute(r,a,c)
        self.assertEqual("BLOCKED",result["status"])
        self.assertEqual("AUTHORITATIVE_STATE_UNAVAILABLE",result["reason_code"])

    def test_authoritative_store_rejects_version_rollback(self):
        a=attempt(); store=runtime.MemoryAuthorityStateStore()
        store.set(a,conditions(state_version=2))
        with self.assertRaisesRegex(ValueError,"AUTHORITY_STATE_ROLLBACK_REJECTED"):
            store.set(a,conditions(state_version=1))

if __name__=="__main__": unittest.main()
