import unittest
from pathlib import Path
import sys, tempfile
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import ambient_runtime as runtime
from test_ambient_runtime import attempt, conditions

class AuthoritativeStateRestartHostileTest(unittest.TestCase):
    def test_authoritative_state_survives_provider_restart(self):
        a=attempt()
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"authority-state.db"

            # Provider instance 1 records authoritative v2 where consent is invalid.
            first=runtime.MemoryAuthorityStateStore()
            first.set(a,conditions(consent_valid=False,state_version=2))

            # Simulate provider/process replacement. A production-grade authority
            # source must recover authoritative state rather than forgetting it.
            restarted=runtime.MemoryAuthorityStateStore()
            recovered=restarted.get(a)

            self.assertIsNotNone(
                recovered,
                "AUTHORITATIVE-STATE DURABILITY FAILURE: provider restart forgot current authority state"
            )
            self.assertEqual(2,recovered.state_version)
            self.assertFalse(recovered.consent_valid)

if __name__=="__main__": unittest.main()
