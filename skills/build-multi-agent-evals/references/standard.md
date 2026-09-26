# Multi-Agent Evaluation Standard

Use a layered suite:

1. Member conformance and existing member risk gates.
2. Interaction contract, authorization, data-flow, and schema tests.
3. Coordination tests for routing, aggregation, budgets, and termination.
4. Durability tests for retries, duplicates, crashes, cancellation, and compensation.
5. Adversarial tests for injection propagation, collusion, false consensus, registry poisoning, and resource exhaustion.
6. End-to-end outcome, cost, latency, and human-impact tests.

Critical risk scenarios are hard gates. Report distributions and tail behavior, not only means. Treat cost per successful outcome and worst-case amplification as first-class metrics.

Every report identifies a system subject and exact composition manifest. Baselines use the same dataset and evaluator version. Dynamic systems report admission decisions and selected members per run.
