FlowSignal™ Runtime Authority Integration Demonstrator (V2)
Purpose

This demonstrator illustrates how an external Clinical Governance system can interoperate with an independent Runtime Authority through an Execution Bind Point.

The demonstrator shows that governance and Runtime Authority answer different questions.

Clinical Governance

↓

Is this action permitted by policy?

↓

Gate Decision Record

↓

FlowSignal Runtime Authority

↓

Is delegated authority still
legitimately exercisable now?

↓

Authority Receipt

↓

Clinical Consequence
Demonstration

The current implementation demonstrates integration with the Mental Health Chat clinical governance engine.

The supplied Gate Decision Record contains:

policy verdict
evaluated conditions
freshness metadata
integrity chain
audit evidence

FlowSignal consumes this evidence independently before determining runtime admissibility.

Architectural Separation
Clinical Governance	FlowSignal Runtime Authority
Applies policy	Determines runtime admissibility
Produces Gate Decision Record	Produces Authority Receipt
Clinical governance	Institutional authority
Policy compliance	Runtime legitimacy
Repository Contents
index.html

gate_decision_export.json

technical_brief.md

verify_chain.py
Current Status
Version

V2 Phase 1

Features

✅ Runtime Integration Pipeline

✅ Clinical Governance Provider

✅ Gate Decision Record

✅ Execution Bind Point

✅ Runtime Authority

⬜ Live JSON Import

⬜ Integrity Verification

⬜ Authority Request Mapping

⬜ Authority Receipt Generation

Roadmap

Phase 1

User Interface

✔ Complete

Phase 2

Import Gate Decision Record

Phase 3

Runtime Authority Mapping

Phase 4

Live Authority Determination


Current demonstration provider: Mental Health Chat (synthetic gate records and technical brief supplied for architectural interoperability evaluation). The demonstrator illustrates the integration pattern and does not represent a production deployment.
