# Multi-Agent Risk Examples

## Authority Laundering

A coordinator persuades a more privileged member to perform an action outside the user's scope. Controls: intersection-based edge authorization, task-scoped credentials, pre-effect revalidation, audit receipts. Tests attempt direct and indirect privilege escalation.

## False Consensus

Multiple agents using the same evidence and model family agree on an incorrect claim. Controls: source-grounded evidence, declared independence assumptions, dissent preservation, calibrated abstention, deterministic escalation.

## Dynamic Admission

A compromised registry offers a compatible-looking agent with broader data access. Controls: authenticated registry, allowlisted publishers, immutable digests, contract and tier checks, quarantine, per-run manifests, and admission-failure fallback.
