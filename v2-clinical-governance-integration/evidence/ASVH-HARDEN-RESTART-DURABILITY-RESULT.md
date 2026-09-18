# ASVH-HARDEN — Restart Durability Result

Date: 2026-09-18
Status: PASS AFTER REMEDIATION

The restart-durability hostile challenge initially failed and the failure remains preserved.

Remediation introduced a durable SQLite-backed receipt-consumption store with a unique token constraint. The challenge was rerun with a new gateway instance against the same durable store.

GitHub Actions run: 35386616668
Head commit: 497b3185ad1d858613e3bba1580e1eb61407dae2
Conclusion: SUCCESS

Classification: **PASS AFTER REMEDIATION**

This demonstrates durable receipt-consumption across gateway object replacement/restart in the reference harness using the same SQLite store. It does not demonstrate distributed multi-host atomicity, production datastore guarantees, or physical EPR route closure.
