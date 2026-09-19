import copy, unittest
from datetime import datetime
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from ambient_runtime import *

def attempt(**kw):
    d=dict(actor_id="clinician-001",patient_id="patient-001",encounter_id="enc-001",
           action="commit_ai_draft_to_epr",content_digest="sha256:draft-a",
           mandate_id="mandate-001",attempted_at="2026-09-18T16:00:00Z")
    d.update(kw); return Attempt(**d)

def conditions(**kw):
    d=dict(identity_verified=True,consent_valid=True,encounter_valid=True,
           clinician_present=True,evidence_fresh=True,documentation_integrity=True,state_version=1)
    d.update(kw); return Conditions(**d)

class SixConditions(unittest.TestCase):
    def test_all_six_hold_allows(self):
        self.assertEqual(ALLOW,evaluate(attempt(),conditions())["decision"])

    def assertRule(self,field,decision,code):
        r=evaluate(attempt(),conditions(**{field:False}))
        self.assertEqual((decision,code),(r["decision"],r["reason_code"]))

    def test_identity_individually(self): self.assertRule("identity_verified",REFUSE,"IDENTITY_NOT_VERIFIED")
    def test_consent_individually(self): self.assertRule("consent_valid",REFUSE,"CONSENT_NOT_VALID")
    def test_encounter_individually(self): self.assertRule("encounter_valid",REFUSE,"ENCOUNTER_NOT_VALID")
    def test_clinician_individually(self): self.assertRule("clinician_present",ESCALATE,"CLINICIAN_NOT_PRESENT")
    def test_freshness_individually(self): self.assertRule("evidence_fresh",ESCALATE,"EVIDENCE_STALE")
    def test_document_integrity_individually(self): self.assertRule("documentation_integrity",REFUSE,"DOCUMENTATION_INTEGRITY_FAILED")

class NowStateTransition(unittest.TestCase):
    def test_state_change_invalidates_old_allow(self):
        a=attempt(); old=conditions(state_version=1); receipt=evaluate(a,old)
        self.assertEqual(ALLOW,receipt["decision"])
        current=conditions(consent_valid=False,state_version=2)
        result=ExecutionGateway().execute(receipt,a,current)
        self.assertEqual(("BLOCKED","AUTHORITY_STATE_STALE_REEVALUATION_REQUIRED"),(result["status"],result["reason_code"]))

    def test_fresh_evaluation_after_change_refuses(self):
        r=evaluate(attempt(),conditions(consent_valid=False,state_version=2))
        self.assertEqual((REFUSE,"CONSENT_NOT_VALID"),(r["decision"],r["reason_code"]))

class WhoWhatMatchBinding(unittest.TestCase):
    def setUp(self):
        self.a=attempt(); self.c=conditions(); self.r=evaluate(self.a,self.c)
    def assertBlocked(self,**mutation):
        x=attempt(**mutation); got=ExecutionGateway().execute(self.r,x,self.c)
        self.assertEqual(("BLOCKED","ACTION_BINDING_MISMATCH"),(got["status"],got["reason_code"]))
    def test_who_actor_substitution(self): self.assertBlocked(actor_id="clinician-999")
    def test_match_patient_substitution(self): self.assertBlocked(patient_id="patient-999")
    def test_match_encounter_substitution(self): self.assertBlocked(encounter_id="enc-999")
    def test_what_action_substitution(self): self.assertBlocked(action="send_message_to_patient")
    def test_match_content_substitution(self): self.assertBlocked(content_digest="sha256:draft-b")
    def test_what_mandate_substitution(self): self.assertBlocked(mandate_id="mandate-999")
    def test_exact_bound_attempt_permits_represented_commit(self):
        self.assertEqual("EPR_COMMIT_PERMITTED",ExecutionGateway().execute(self.r,self.a,self.c)["status"])

if __name__=="__main__": unittest.main()
