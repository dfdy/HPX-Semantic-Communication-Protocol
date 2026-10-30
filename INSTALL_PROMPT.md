# HPX-SCP v0.5.0 installation instructions for a development agent

Review the proposed kit against existing HPX specifications and permissions. Do not silently overwrite other authoritative documents. Do not activate this governance revision until the repository owner explicitly approves it. Integrate the provided `AGENTS.md.fragment` into existing instructions without deleting narrower local rules.

**Critical change:** human-readable `PROTOCOL.md` remains canonical but MUST NOT be loaded into ordinary agent context. Run `python3 scripts/protocol_context.py --for <task-scope>` as an independent verification process; use only its verified, minimal YAML output as protocol prompting. Default includes kernel and baseline; expand scopes/record kinds when the task requires them. Never dump the whole appendix, omit applicable constraints, or fallback to unverified data when the SHA-256 / deterministic projection fails.

Run bootstrap, record validation, and tests; report actual outcomes. Preserve legacy records. For protocol changes edit canonical text first, regenerate, then verify. Compatible changes are delegated; breaking, kernel, security and governance changes require owner approval. No tool permissions or application specification authority are changed.

The verifier checks exactly two on-file region digests (natural and machine) plus deterministic projection correspondence. Do not include hashes or the canonical prose in ordinary agent instructions. Rebuild the semantic YAML and manifest together after an authorised prose edit.
