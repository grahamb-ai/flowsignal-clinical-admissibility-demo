# V2 Health Hardening + AiRP Experimental Baseline

Status: FROZEN PRE-CHANGE BASELINE
Date: 2026-09-18
Base branch: main
Working branch: v2-health-hardening-airp
Baseline path: v2-clinical-governance-integration/

## Purpose
Preserve the state of V2 before health hardening, regression testing, NHS ambient-scribing scenarios, and experimental AiRP assurance-context work.

## Baseline observations
The V2 demonstrator already represents:
Clinical Governance -> Gate Decision Record -> Execution Bind Point -> FlowSignal Runtime Authority -> Authority Receipt -> Clinical Consequence.

The existing UI includes NHS Ambient Scribing as a selectable provider.

At freeze, README marks V2 as Phase 1 and lists Live JSON Import, Integrity Verification, Authority Request Mapping, and Authority Receipt Generation as incomplete. gate_decision_export.json and verify_chain.py are placeholder/empty files.

## Claim boundary
This branch is an experimental reference demonstrator. A PASS may establish only the behaviour exercised by the named test on the represented harness surface. It does not establish physical non-formation, universal non-bypassability, production safety, clinical efficacy, regulatory compliance, or control of an external EPR unless separately demonstrated.

## Failure preservation rule
FAIL -> preserve evidence -> diagnose -> remediate -> rerun the same test -> record PASS AFTER REMEDIATION where applicable.
Historical failures must not be rewritten or deleted.
