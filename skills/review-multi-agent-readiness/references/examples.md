# Multi-Agent Readiness Examples

## Blocker

`[P0] System allows recursive delegation but has no enforced depth or total-run ceiling.` Evidence shows the spec declares recursion while runtime tests demonstrate continued child creation. Recommendation: no-go until workflow enforcement and exhaustion evals pass.

## Conditional Finding

`[P2] Cost alert has no production paging route.` Hard cost ceilings are enforced and release gates pass, so launch may be conditional on assigning an operational owner and paging route before a dated limited rollout.

## Evidence Gap

A threat model claims injection isolation, but no data-flow policy or adversarial propagation eval is present. Report the control as unverified; do not credit it in residual risk.
