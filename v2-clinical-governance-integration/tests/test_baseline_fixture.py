import copy
import json
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from verify_chain import verify

FIXTURE=json.loads((ROOT/"gate_decision_export.json").read_text(encoding="utf-8"))

class BaselineFixtureTests(unittest.TestCase):
    def test_fixture_passes(self):
        self.assertEqual([],verify(copy.deepcopy(FIXTURE)))

    def test_empty_records_fails(self):
        d=copy.deepcopy(FIXTURE); d["records"]=[]
        self.assertTrue(verify(d))

    def test_missing_metadata_fails(self):
        d=copy.deepcopy(FIXTURE); del d["export_metadata"]["provider"]
        self.assertTrue(any("metadata missing" in e for e in verify(d)))

    def test_unknown_verdict_fails(self):
        d=copy.deepcopy(FIXTURE); d["records"][0]["verdict"]="ALLOW"
        self.assertTrue(any("verdict invalid" in e for e in verify(d)))

    def test_duplicate_record_id_fails(self):
        d=copy.deepcopy(FIXTURE); d["records"][1]["record_id"]=d["records"][0]["record_id"]
        self.assertTrue(any("duplicate" in e for e in verify(d)))

    def test_missing_required_condition_fails(self):
        d=copy.deepcopy(FIXTURE); d["records"][0]["conditions"]=d["records"][0]["conditions"][:-1]
        self.assertTrue(any("conditions missing" in e for e in verify(d)))

    def test_approved_with_failed_condition_fails(self):
        d=copy.deepcopy(FIXTURE); d["records"][0]["conditions"][1]["pass"]=False
        self.assertTrue(any("APPROVED despite" in e for e in verify(d)))

    def test_blocked_record_with_failed_condition_is_structurally_valid(self):
        self.assertEqual([],verify({"export_metadata":FIXTURE["export_metadata"],"records":[FIXTURE["records"][1]]}))

if __name__=="__main__": unittest.main()
