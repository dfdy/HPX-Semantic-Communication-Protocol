# HPX-SCP changelog

## 0.5.0 — Continuity, shared amendments, dual-hash verification (proposed)

- Uses deterministic, indentation-based YAML for the appended semantic representation and default scoped agent packets; preserves JSON records and an optional JSON packet compatibility mode.
- Adds recovery across context compaction via persistent non-authoritative checkpoints and fresh verified context packets.
- Requires applied autonomous protocol extensions to be integrated into canonical prose and indexed for discovery.
- Replaces per-rule and per-section hashes with **two** manifest hashes: canonical prose SHA-256 and semantic YAML SHA-256.
- Hashes both regions separately, then checks exact deterministic correspondence of the semantic YAML to the canonical prose; all checks run outside model context.
- Removes digest metadata from ordinary model packets and the shared amendment registry.
- Retains owner approval for breaking, security, authority and governance changes.


## 0.4.0 — Minimum Sufficient Protocol (proposed)

- Retains canonical human-readable primacy but bars its inclusion in ordinary model context.
- Introduces a short, human-readable Minimum Sufficient Protocol with 41 separately tagged rules.
- Replaces the v1 redundant full-section semantic projection with a v2 derived compact appendix (rules, sections digests, typed vocabulary; no complete duplicated prose).
- Adds an independent `protocol_context.py` that verifies the canonical document and outputs only selected rule scopes, requested record types and relationships.
- Adds explicit Minimum Sufficient Context, context expansion, handoff-delta, measurement, and fail-closed packet constraints.
- Adds v0.4.0 to record schema while retaining v0.1.0–v0.3.0 record support.
- The ordinary packet includes five kernel rules and the baseline; detailed verification mechanics are available in the on-demand `preflight` scope.
- Rejects untagged canonical prose that would otherwise disappear from the machine projection.
- Retains agent-compatible extension delegation and owner-only governance amendments.
- Changes normal agent prompt-loading behaviour and verification mechanism; requires owner approval before adoption.

## Previous versions

v0.3.0: canonical prose, protected SHA-256, deterministic semantic projection, five-rule bootstrap kernel.

v0.2.0: controlled autonomous protocol extensions, `protocol_change` records.

v0.1.0: seven original persistent record types, validation and evidence-aware handoffs.
