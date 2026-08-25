# Mentor Defense — Day 23

## 1. Why is this core action closer to value than `ask_ai`?

AI output can inform a review without producing a disposition. Value becomes observable only when the analyst completes a valid terminal resolution and the required rationale/evidence is persisted for the case.

## 2. Why is raw daily active usage a weak metric here?

Case demand is externally generated. More sessions or more dashboard opens can mean more browsing, repeated work or more fraud volume; neither proves a defensible resolution.

## 3. What is the natural trigger?

A suspicious transaction creates an eligible fraud case and that case is assigned or becomes available to the analyst.

## 4. Why does a notification not define retention?

The notification is only a delivery mechanism. The reason to return is a new eligible case and the analyst’s operational responsibility to resolve it.

## 5. Why is the retention window custom/event-based?

The action follows case opportunities, not a guaranteed calendar rhythm. Analysts without eligible workload must not be marked churned for an opportunity they never received.

## 6. What is the NSM quality threshold?

The case must have a valid terminal disposition, required decision information and rationale/evidence references persisted, with required evidence completed before resolution and no duplicate resolution version.

## 7. What can cause the NSM to rise while product quality falls?

Analysts can resolve more cases while producing decisions that are later reopened or reversed. Reopen rate and reversal rate are therefore counter-metrics.

## 8. Why does `fraud_case_resolved` fire after persistence rather than button click?

A click expresses intent. The product value and audit evidence exist only after the state transition and required fields are saved successfully.

## 9. How are duplicate events prevented?

Each completion has an idempotency key such as `case_id + resolution_version`; reloads, retries and duplicate submissions must resolve to one logical event.

## 10. Why exclude periods with no eligible cases?

No case means no natural opportunity to perform the action. That period is unobserved workload, not evidence that the analyst rejected product value.

## 11. What would falsify the loop hypothesis?

If high-quality resolution rate does not improve across the next three eligible opportunities for comparable activated analysts, or improves while reopen/reversal rates deteriorate, the hypothesis is not supported.

## 12. What did AI help with, and what did the student decide personally?

AI helped brainstorm the action, cadence, metric hypothesis, event model and logic checks. The student personally selected Core Action A, Cadence A and Metric Hypothesis A, and supplied the reflection in [ai-support-log.md](./ai-support-log.md).
