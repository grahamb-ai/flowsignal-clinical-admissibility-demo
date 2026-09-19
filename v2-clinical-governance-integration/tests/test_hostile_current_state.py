import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import ambient_runtime as runtime
from test_ambient_runtime import attempt, conditions

class CallerSuppliedCurrentStateHostileTest(unittest.TestCase):
    def test_caller_cannot_replay_stale_coherent_state_as_current(self):
        a=attempt()
        t0=conditions(consent_valid=True,state_version=1)
        receipt=runtime.evaluate(a,t0)
        self.assertEqual(runtime.ALLOW,receipt["decision"])

        # Authoritative reality has changed: consent is no longer valid at v2.
        authoritative_now=conditions(consent_valid=False,state_version=2)
        self.assertEqual(runtime.REFUSE,runtime.evaluate(a,authoritative_now)["decision"])

        # The gateway owns the final NOW lookup. Authoritative state is v2.
        state_store=runtime.MemoryAuthorityStateStore()
        state_store.set(a,authoritative_now)
        gateway=runtime.ExecutionGateway(state_provider=state_store)

        # Hostile caller lies by supplying the old coherent v1 snapshot as "current".
        # The gateway must ignore it and use its authoritative state provider.
        attacker_supplied_current=conditions(consent_valid=True,state_version=1)
        result=gateway.execute(receipt,a,attacker_supplied_current)

        self.assertNotEqual(
            "EPR_COMMIT_PERMITTED",result["status"],
            "CURRENT-STATE TRUST FAILURE: caller supplied stale coherent state and gateway permitted consequence"
        )

if __name__=="__main__": unittest.main()
