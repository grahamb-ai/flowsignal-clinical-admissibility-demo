# TEST_PLAN

Status: INITIAL
Date: 2026-09-18

## Verification ladder

### L0 — Baseline / boring correctness
- valid inputs and expected ALLOW
- expected ESCALATE
- expected REFUSE
- missing/malformed fields
- timestamp validation
- unknown actor/mandate
- duplicate request behaviour
- deterministic repeatability

### L1 — NHS ambient-scribing rule tests
Independently exercise identity, consent, encounter validity, clinician presence, evidence freshness, and documentation integrity. Each negative case must identify the responsible rule.

### L2 — State transition / NOW
Establish authority at T0, mutate one material condition at T1, attempt represented consequence at T2, and prove stale standing cannot be silently reused.

### L3 — Binding / WHO-WHAT-MATCH
Actor, patient/target, encounter, action/content, mandate and other consequence-relevant substitutions.

### L4 — Evidence integrity
Authority Receipt required fields, reason codes, action binding, integrity/tamper detection, immutable historical record, replay/reconstruction claim boundary.

### L5 — Hardening / hostile
Stale authority, coherent rollback, replay, evidence tampering, bypass/route closure, fail-open attempts, race/TOCTOU, duplicate execution, escalation unavailable, gateway failure.

### L6 — Whole-stack represented consequence
Do not stop at evaluate() returning REFUSE. Attempt the represented EPR consequence and establish whether the governed route prevents the represented commit. External EPR non-bypassability remains NOT DEMONSTRATED until actually tested.

### L7 — AiRP experimental context
Run materially identical scenario with runtime control absent vs present. Surface generated FlowSignal evidence as a candidate Step 5 control artefact. Display Step 6 as NOT DETERMINED — ORCHA assessment required.

## Result vocabulary
PASS
FAIL
PASS AFTER REMEDIATION
NOT DEMONSTRATED
OUT OF SCOPE
EXPERIMENTAL

No stronger claim may be inferred from a result than the test actually establishes.
