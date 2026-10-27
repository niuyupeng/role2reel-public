# Atomic shot gate

Decide whether a storyboard row is one executable shot or a deliberately designed continuous-shot cluster before estimating duration. A longer row is not automatically wrong, and a short row is not automatically atomic. Apply this gate to cinematic shots, not provider generation units: one generation unit may contain several shots, with one row per actual cut in the internal plan. A multi-shot generation segment does not require cluster approval merely because it contains multiple beats or cuts.

## Atomicity test

An `ATOMIC_PASS` row has one dominant audience task, one continuous camera/geography contract, one main causal path, and one ending state that the next shot can inherit. Its internal beats may still include preparation, a line, a look, contact, or a brief hold. Several connected beats or exchanges within that continuous view do not by themselves require a split or an approval.

Mark `SPLIT_REQUIRED` when the row contains independent camera locations or axes, unrelated cause/result chains, a hidden location change, a subject switch that needs a new audience task, or an action whose contact and result cannot remain readable in one view. Mark `SPLIT_RECOMMENDED` when the row is technically possible but its reaction, joke, reveal, or physical consequence would be clearer as separate cuts.

Use `CLUSTER_APPROVAL_REQUIRED` only for a proposed continuous-shot exception that would replace an author-locked cut or shot boundary, or otherwise change a protected source constraint. Record the beat sequence, camera continuity, start/end state, the affected constraint and the author's decision. An existing explicit request for that continuous shot is already the decision; do not ask again. A continuous shot designed within the user's authorized scope, or a provider unit that groups separately planned shots, does not create an additional approval step. Never use cluster status to excuse an impossible camera path, unreadable contact/result or hidden cut; repair those defects before production lock.

## Cause and consequence

For a physical action, keep the readable path `prepare or decide → approach → contact or trigger → force/state change → recovery/result`. For a performance beat, keep `stimulus → comprehension → involuntary response → chosen mask or tactic → visible residue`. A line can share a shot with an action, but it must not make the audience miss the listener's understanding or the object's result.

Only after this gate should the timing plan calculate hard floors and provider duration. `SPLIT_REQUIRED` and unapproved `CLUSTER_APPROVAL_REQUIRED` block production lock; `SPLIT_RECOMMENDED` stays visible as a repair decision rather than being silently ignored.

Use [source-truth-gate.md](source-truth-gate.md) first. For a persistent production audit, record the outcome in [shot-readiness-review.yaml](../assets/templates/shot-readiness-review.yaml); for a compact review, keep the finding and its source basis in the existing review notes without creating an additional file requirement.
