#!/usr/bin/env python3
"""Baseline structural verifier for V2 synthetic Gate Decision exports.

This verifier deliberately proves only structural invariants of the local
synthetic fixture. It does not verify a production signature, clinical
correctness, external EPR behaviour, or ORCHA/AiRP conformance.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

REQUIRED_META = {"provider","gate_version","policy_ref","exported_at","integrity_scheme"}
REQUIRED_RECORD = {"record_id","verdict","reason","conditions"}
ALLOWED_VERDICTS = {"APPROVED","BLOCKED"}
REQUIRED_CONDITIONS = {
    "identity_verified","consent_valid","encounter_valid",
    "clinician_present","evidence_fresh","documentation_integrity",
}

def verify(doc: object) -> list[str]:
    errors=[]
    if not isinstance(doc,dict): return ["root must be an object"]
    meta=doc.get("export_metadata")
    records=doc.get("records")
    if not isinstance(meta,dict): errors.append("export_metadata must be an object")
    else:
        missing=REQUIRED_META-meta.keys()
        if missing: errors.append("metadata missing: "+", ".join(sorted(missing)))
    if not isinstance(records,list) or not records:
        errors.append("records must be a non-empty array")
        return errors
    seen=set()
    for i,r in enumerate(records):
        p=f"records[{i}]"
        if not isinstance(r,dict): errors.append(f"{p} must be an object"); continue
        missing=REQUIRED_RECORD-r.keys()
        if missing: errors.append(f"{p} missing: "+", ".join(sorted(missing)))
        rid=r.get("record_id")
        if not isinstance(rid,str) or not rid: errors.append(f"{p}.record_id must be non-empty")
        elif rid in seen: errors.append(f"{p}.record_id duplicate: {rid}")
        else: seen.add(rid)
        if r.get("verdict") not in ALLOWED_VERDICTS: errors.append(f"{p}.verdict invalid")
        cs=r.get("conditions")
        if not isinstance(cs,list): errors.append(f"{p}.conditions must be an array"); continue
        names=set()
        for j,c in enumerate(cs):
            if not isinstance(c,dict) or not isinstance(c.get("name"),str) or not isinstance(c.get("pass"),bool):
                errors.append(f"{p}.conditions[{j}] requires string name and boolean pass"); continue
            names.add(c["name"])
        missing_conditions=REQUIRED_CONDITIONS-names
        if missing_conditions: errors.append(f"{p} conditions missing: "+", ".join(sorted(missing_conditions)))
        failed=[c["name"] for c in cs if isinstance(c,dict) and c.get("pass") is False]
        if r.get("verdict")=="APPROVED" and failed: errors.append(f"{p} APPROVED despite failed condition(s): "+", ".join(failed))
    return errors

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("path",nargs="?",default=str(Path(__file__).with_name("gate_decision_export.json")))
    args=ap.parse_args()
    try: doc=json.loads(Path(args.path).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAIL: cannot load JSON: {e}"); return 2
    errors=verify(doc)
    if errors:
        print("FAIL")
        for e in errors: print(f"- {e}")
        return 1
    print(f"PASS: structural fixture verified ({len(doc['records'])} records)")
    print("CLAIM BOUNDARY: structural local fixture only; cryptographic authenticity and external consequence control NOT DEMONSTRATED.")
    return 0
if __name__=="__main__": sys.exit(main())
