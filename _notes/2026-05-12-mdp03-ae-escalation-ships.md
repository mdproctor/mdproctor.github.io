---
layout: post
title: "Adverse event escalation ships"
date: 2026-05-12
type: phase-update
entry_type: note
subtype: diary
projects: [casehub-clinical]
excerpt: "Adverse event escalation merges to main — the SLA wiring, WorkItem creation, and ledger entries are live, with protocol deviation PI authorisation next."
---

Adverse event escalation is in main.

The previous entry covered what we built — SLA deadlines keyed to CTCAE grade, WorkItem
creation, ledger entries in the same JTA transaction. The merge was clean. Nothing surfaced
that wasn't already known.

What's next is protocol deviation PI authorisation. The COMMAND lifecycle is already in
the foundation. The clinical layer goes on top.

Engine#112 — sub-case execution wiring — is still open, which keeps the multi-site
scenario on hold. That one needs engine work before this repo can touch it.
