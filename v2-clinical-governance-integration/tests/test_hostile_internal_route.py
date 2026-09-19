import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import ambient_runtime as runtime
from test_ambient_runtime import attempt, conditions

class InternalRouteClosureHostileTest(unittest.TestCase):
    def test_internal_helper_cannot_form_represented_consequence(self):
        a=attempt(); c=conditions(); r=runtime.evaluate(a,c)
        gateway=runtime.ExecutionGateway()
        first=gateway.execute(r,a,c)
        self.assertEqual("EPR_COMMIT_PERMITTED", first["status"])

        bypass=runtime._execute_unconsumed(r,a,c)
        self.assertNotEqual(
            "EPR_COMMIT_PERMITTED", bypass["status"],
            "ROUTE CLOSURE FAILURE: internal helper formed represented consequence outside ExecutionGateway"
        )

if __name__=="__main__": unittest.main()
