# Instructions for installing HPX-SCP v0.6.0 in a development repository

Integrate this kit as a **bidirectional inter-agent prompting protocol**, not as a general agent-instruction framework. Preserve and review existing HPX specification authority; do not overwrite AGENTS.md, CODEOWNERS or other project instructions. Merge `AGENTS.md.fragment` narrowly.

Install `PyYAML>=6,<7` and `jsonschema>=4.18,<5`. Check `python3 scripts/bootstrap_semantic_protocol.py`, `python3 scripts/protocol_amendments.py validate`, `python3 scripts/validate_semantic_records.py`, and `python3 -m unittest discover -s tests -p 'test_*.py'`.

When an agent is instructed to communicate with another using SCP, it must (1) discover support, (2) transfer the verified protocol outside model context when needed, (3) require a successful readiness exchange, and (4) send subsequent tasks and results in schema-checked YAML in both directions. Use the file-based `scripts/scp_wire.py` CLI for reference; integrate actual agent invocation/transport only where the repository has an authorised communication channel. Do not claim automatic network discovery, authentication, or automatic installation of untrusted protocol bundles.

Canonical Markdown remains sole authority. Regenerate YAML and both digests only after approved prose changes; require owner review for governance or breaking changes. Preserve old JSON record compatibility and ensure all contexts remain minimum sufficient. Report any failure to establish a peer session explicitly.
