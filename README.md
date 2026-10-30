# HPX-SCP v0.5.0 — Minimum Sufficient Protocol

**Proposed, not yet adopted.** Human-readable text is the sole canonical policy; the appended machine representation is subordinate and is never injected wholesale into an agent prompt.

## Purpose

Minimise repeated context and interpretation across development agents while retaining human-readable oversight and exact source authority. A standalone verifier reads and hashes canonical prose **outside model context**, verifies the derived semantic representation, and emits only scoped semantic instructions to the requesting agent.

## Usage

From the repository root:

```bash
python3 scripts/bootstrap_semantic_protocol.py
python3 scripts/protocol_context.py --for implement
python3 scripts/protocol_context.py --for verify --record-type verification_result
python3 scripts/protocol_context.py --for handoff --record-type handoff
python3 scripts/protocol_context.py --for amend --record-type protocol_change
```

All packets include the kernel and baseline. The loader emits scoped, indented YAML with only relevant rule IDs/directives and requested record/relation definitions. The full natural-language source **is never printed**. An agent can request more scopes when needed; minimum context never permits missing authoritative constraints.

## Adoption

1. Review this proposed governance revision before activation, since it replaces v0.3's bootstrap/projection and normal agent-loading policy.
2. Copy the kit into HPX without overwriting independent authoritative files; merge `AGENTS.md.fragment` into existing agent guidance.
3. Install `python3 -m pip install 'jsonschema>=4.18,<5' 'PyYAML>=6,<7'`, then run the bootstrap and tests.
4. Retain existing v0.1.0–v0.3.0 records without rewriting their `protocol_version`.
5. Restrict repository ownership of the canonical policy and verifier; optionally provide `--trusted-sha256` or owner-managed `HPX_SCP_TRUSTED_SHA256` outside the writable repository.

If an existing consumer still requires JSON packets, use `--format json`. Historical JSON record files remain unchanged.

## Amendments

Edit canonical prose first; then regenerate the appendix and test:

```bash
python3 scripts/rebuild_semantic_appendix.py
python3 scripts/bootstrap_semantic_protocol.py
python3 scripts/validate_semantic_records.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Only compatible changes are delegated; breaking or governance changes require owner approval. Matching manifest hashes establish integrity, and deterministic regeneration establishes correspondence; neither establishes author authenticity. This protocol is an engineering communication convention, not HPX runtime schema, permission escalation, or a replacement for application specifications.

## Minimal dual-hash gate

`PROTOCOL.md` contains canonical Markdown, a derived semantic YAML appendix, and an external integrity manifest with exactly **two** SHA-256 values (one for each region). The verifier checks both digests and regenerates the expected machine YAML from canonical prose; no section or rule has its own hash. Hashes are never emitted into ordinary agent packets.
