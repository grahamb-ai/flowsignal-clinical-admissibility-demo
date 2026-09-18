"""NHS ambient-scribing Runtime Authority reference engine.

Reference-harness semantics only. This module does not establish clinical
correctness, production EPR enforcement, regulatory compliance, or universal
non-bypassability.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib, hmac, json, sqlite3, threading

ALLOW="ALLOW"; ESCALATE="ESCALATE"; REFUSE="REFUSE"

@dataclass(frozen=True)
class Attempt:
    actor_id:str
    patient_id:str
    encounter_id:str
    action:str
    content_digest:str
    mandate_id:str
    attempted_at:str

@dataclass(frozen=True)
class Conditions:
    identity_verified:bool
    consent_valid:bool
    encounter_valid:bool
    clinician_present:bool
    evidence_fresh:bool
    documentation_integrity:bool
    state_version:int=1

RULES=(
 ("identity_verified",REFUSE,"IDENTITY_NOT_VERIFIED"),
 ("consent_valid",REFUSE,"CONSENT_NOT_VALID"),
 ("encounter_valid",REFUSE,"ENCOUNTER_NOT_VALID"),
 ("clinician_present",ESCALATE,"CLINICIAN_NOT_PRESENT"),
 ("evidence_fresh",ESCALATE,"EVIDENCE_STALE"),
 ("documentation_integrity",REFUSE,"DOCUMENTATION_INTEGRITY_FAILED"),
)

def canonical(obj)->str:
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def binding_hash(a:Attempt)->str:
    # attempted_at is deliberately excluded: the consequence identity is bound,
    # while freshness/current standing are evaluated separately at attempt time.
    d=asdict(a); d.pop("attempted_at")
    return hashlib.sha256(canonical(d).encode()).hexdigest()

def evaluate(a:Attempt,c:Conditions,secret:bytes=b"synthetic-test-key")->dict:
    for field,outcome,code in RULES:
        if not getattr(c,field):
            return _receipt(a,c,outcome,code,secret)
    return _receipt(a,c,ALLOW,"AUTHORITY_CURRENT_AND_ACTION_MATCHED",secret)

def _receipt(a,c,outcome,code,secret):
    body={"attempt":asdict(a),"conditions":asdict(c),"decision":outcome,
          "reason_code":code,"action_binding_hash":binding_hash(a)}
    sig=hmac.new(secret,canonical(body).encode(),hashlib.sha256).hexdigest()
    return {**body,"integrity":{"algorithm":"HMAC-SHA256","value":sig}}

def verify_receipt(r:dict,secret:bytes=b"synthetic-test-key")->bool:
    try:
        body={k:v for k,v in r.items() if k!="integrity"}
        expected=hmac.new(secret,canonical(body).encode(),hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected,r["integrity"]["value"])
    except (KeyError,TypeError):
        return False

class MemoryConsumptionStore:
    def __init__(self):
        self._consumed=set(); self._lock=threading.Lock()
    def claim(self,token:str)->bool:
        with self._lock:
            if token in self._consumed: return False
            self._consumed.add(token); return True

class SQLiteConsumptionStore:
    """Durable reference store; a unique token provides atomic claiming."""
    def __init__(self,path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS consumed_receipts (token TEXT PRIMARY KEY)")
    def claim(self,token:str)->bool:
        try:
            with sqlite3.connect(self.path,timeout=5) as db:
                db.execute("INSERT INTO consumed_receipts(token) VALUES (?)",(token,))
            return True
        except sqlite3.IntegrityError:
            return False

class ExecutionGateway:
    def __init__(self,store=None):
        self.store=store or MemoryConsumptionStore()
    def execute(self,bound_receipt:dict,attempted:Attempt,current:Conditions)->dict:
        result=_execute_unconsumed(bound_receipt,attempted,current)
        if result["status"]!="EPR_COMMIT_PERMITTED": return result
        token=bound_receipt.get("integrity",{}).get("value")
        if not token or not self.store.claim(token):
            return {"status":"BLOCKED","reason_code":"AUTHORITY_RECEIPT_ALREADY_CONSUMED"}
        return result

def execute(bound_receipt:dict, attempted:Attempt, current:Conditions)->dict:
    """Stateless compatibility helper; one-time use requires ExecutionGateway."""
    return _execute_unconsumed(bound_receipt,attempted,current)

def _execute_unconsumed(bound_receipt:dict, attempted:Attempt, current:Conditions)->dict:
    """Represented EPR gateway. Fresh evaluation is mandatory before commit."""
    if not verify_receipt(bound_receipt):
        return {"status":"BLOCKED","reason_code":"RECEIPT_INTEGRITY_FAILED"}
    if bound_receipt["action_binding_hash"] != binding_hash(attempted):
        return {"status":"BLOCKED","reason_code":"ACTION_BINDING_MISMATCH"}
    if bound_receipt["conditions"]["state_version"] != current.state_version:
        return {"status":"BLOCKED","reason_code":"AUTHORITY_STATE_STALE_REEVALUATION_REQUIRED"}
    fresh=evaluate(attempted,current)
    if fresh["decision"]==ALLOW:
        return {"status":"EPR_COMMIT_PERMITTED","reason_code":fresh["reason_code"],"receipt":fresh}
    return {"status":"BLOCKED","reason_code":fresh["reason_code"],"receipt":fresh}
