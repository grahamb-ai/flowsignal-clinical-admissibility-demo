import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import ambient_runtime as runtime
from test_ambient_runtime import attempt, conditions

class RouteClosureHostileTest(unittest.TestCase):
    def test_stateless_compatibility_path_cannot_bypass_single_use_gateway(self):
        """
        RED ATTACK: after a receipt has been consumed through ExecutionGateway,
        attempt the same represented consequence through the module-level
        compatibility execute() path.

        If this returns EPR_COMMIT_PERMITTED, represented route closure is false.
        """
        a=attempt(); c=conditions(); r=runtime.evaluate(a,c)
        gateway=runtime.ExecutionGateway()
        first=gateway.execute(r,a,c)
        self.assertEqual("EPR_COMMIT_PERMITTED",first["status"])

        bypass=runtime.execute(r,a,c)
        self.assertNotEqual(
            "EPR_COMMIT_PERMITTED",bypass["status"],
            "ROUTE CLOSURE FAILURE: stateless execute() bypassed receipt consumption"
        )

if __name__=="__main__": unittest.main()
