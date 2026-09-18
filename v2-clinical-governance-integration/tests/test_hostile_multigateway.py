import os, tempfile, threading, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from ambient_runtime import *
from test_ambient_runtime import attempt, conditions

class MultiGatewayAtomicity(unittest.TestCase):
    def test_two_gateways_shared_store_only_one_commit(self):
        a=attempt(); c=conditions(); r=evaluate(a,c)
        with tempfile.TemporaryDirectory() as d:
            db=os.path.join(d,"shared.db")
            g1=ExecutionGateway(SQLiteConsumptionStore(db))
            g2=ExecutionGateway(SQLiteConsumptionStore(db))
            barrier=threading.Barrier(3); results=[]; lock=threading.Lock()
            def submit(g):
                barrier.wait()
                out=g.execute(r,a,c)
                with lock: results.append(out["status"])
            t1=threading.Thread(target=submit,args=(g1,))
            t2=threading.Thread(target=submit,args=(g2,))
            t1.start(); t2.start(); barrier.wait(); t1.join(); t2.join()
            self.assertEqual(1,results.count("EPR_COMMIT_PERMITTED"),
                             "Two gateways sharing a store must not both permit the same receipt")
            self.assertEqual(1,results.count("BLOCKED"))

    def test_invalid_bound_attempt_does_not_consume_receipt(self):
        a=attempt(); c=conditions(); r=evaluate(a,c)
        with tempfile.TemporaryDirectory() as d:
            g=ExecutionGateway(SQLiteConsumptionStore(os.path.join(d,"shared.db")))
            bad=Attempt(**{**a.__dict__,"patient_id":"patient-other"})
            self.assertEqual("BLOCKED",g.execute(r,bad,c)["status"])
            self.assertEqual("EPR_COMMIT_PERMITTED",g.execute(r,a,c)["status"])

if __name__=="__main__": unittest.main()
