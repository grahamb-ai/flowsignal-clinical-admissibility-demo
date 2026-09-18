import threading, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from ambient_runtime import *
from test_ambient_runtime import attempt, conditions

class NextHostileBoundaryTests(unittest.TestCase):
    def test_restart_does_not_preserve_consumption_state(self):
        # RED: process-local consumption is lost when a new gateway instance is created.
        a=attempt(); c=conditions(); r=evaluate(a,c)
        first=ExecutionGateway()
        self.assertEqual("EPR_COMMIT_PERMITTED",first.execute(r,a,c)["status"])
        restarted=ExecutionGateway()
        self.assertNotEqual("EPR_COMMIT_PERMITTED",restarted.execute(r,a,c)["status"],
            "FAILURE: receipt consumption is not durable across gateway restart")

    def test_concurrent_double_submit_only_one_commit(self):
        # Attack exactly-once behaviour under simultaneous duplicate submissions.
        a=attempt(); c=conditions(); r=evaluate(a,c); gateway=ExecutionGateway()
        barrier=threading.Barrier(3); results=[]
        def submit():
            barrier.wait()
            results.append(gateway.execute(r,a,c)["status"])
        t1=threading.Thread(target=submit); t2=threading.Thread(target=submit)
        t1.start(); t2.start(); barrier.wait(); t1.join(); t2.join()
        self.assertEqual(1,results.count("EPR_COMMIT_PERMITTED"),
            "Exactly one concurrent submission may reach represented commit")
        self.assertEqual(1,results.count("BLOCKED"))

if __name__=="__main__": unittest.main()
