**In short:** HPX-SCP keeps people responsible for what the rules mean, tools responsible for checking their integrity, and agents focused on the minimum verified instructions they need.

# Hypergraph PX Semantic Communication Protocol (HPX-SCP)

**A shared YAML language for agents to prompt each other clearly, with minimal context.**

**Version:** 0.6.0 · **Status:** proposed integration package; not installed in HPX.

## Why it exists

Development agents often pass one another long prompts, recreate context, or interpret the same instruction differently. HPX-SCP gives them a compact, shared way to **ask, answer, clarify, report and hand work off**. Once they have established the protocol, both agents send and receive structured YAML instead of repeatedly explaining their communication conventions.

The point is *inter-agent prompting*. Hash verification, record keeping, context recovery and agent-maintained amendments support that exchange; they are not substitutes for it.

## The idea in one minute

1. **Discover:** An agent instructed to use HPX-SCP sends the other agent a small YAML `hello`. Why? It must not assume its partner already knows the protocol.
2. **Propagate if needed:** If the recipient replies `need`, send the complete protocol as a separate bundle—not as a long language-model prompt. Why? A new partner needs the same definitions before receiving an SCP task.
3. **Verify and agree:** The recipient uses independently trusted tools to check the human-canonical Markdown, its appended semantic YAML, two hashes and version. It replies `ready` only for a matching verified protocol. Why? Agreement about meaning matters more than matching syntax.
4. **Prompt in both directions:** Agents exchange validated YAML `request`, `response`, `clarification`, `error`, `handoff` and `amendment_notice` messages. Why? Shared structures reduce interpretive and context overhead.
5. **Recover and evolve:** Reload verified scopes after compaction; register compatible extensions in the shared protocol. Why? Collaboration must survive sessions and improve without creating private dialects.

```text
Agent A           permitted transport          Agent B
  |-- hello ------------------------------->|
  |<---------------------- ready / need ----|
  |-- verified bundle (if needed) -------->|
  |               [verify / install via trusted tooling]
  |<------------------------------ ready ---|
  |-- YAML request ------------------------>|
  |<------------------------ YAML response -|
```

## What a message looks like

```yaml
scp: HPX-SCP
version: 0.6.0
kind: request
id: m-001
sender: architect
recipient: implementer
conversation: dissertation-editor
body:
  action: implement
  target: ClosedComposition
  requirements: [REQ-031, REQ-042]
  constraints: [preserve_revision_history]
```

The reply is another YAML message with `kind: response`, a `reply_to: m-001` reference, and an outcome such as `status: completed`. The sender must not invent evidence or claim tests passed without running them.

**Why YAML?** It retains the readable, indented form of a semantic sketch while allowing strict validation. YAML is the *required* inter-agent message format; historical durable records remain schema-validated JSON for backward compatibility.

## Try a local two-agent exchange

Requires Python 3, `PyYAML>=6,<7` and `jsonschema>=4.18,<5`.

Run in the kit root. Treat `state-a` and `state-b` as separate agents' local state directories; the files stand in for any permitted communication channel.

```bash
# 1. Verify the human-canonical specification and its YAML projection.
python3 scripts/bootstrap_semantic_protocol.py

# 2. Initiator creates hello.yaml (contains control-plane fingerprint).
python3 scripts/scp_wire.py hello --sender architect --recipient implementer \
  --conversation demo --state-dir state-a --output hello.yaml

# 3. Recipient checks its own protocol and creates ready.yaml (or need.yaml).
python3 scripts/scp_wire.py answer-hello --local implementer \
  --state-dir state-b --input hello.yaml --output ready.yaml

# 4. Initiator accepts the reply; no normal task messages before this.
python3 scripts/scp_wire.py accept-ready --local architect \
  --state-dir state-a --input ready.yaml

# 5. Prepare a YAML body: action: implement, target: ClosedComposition.
printf 'action: implement\ntarget: ClosedComposition\n' > request-body.yaml

python3 scripts/scp_wire.py send --kind request --sender architect \
  --recipient implementer --conversation demo --state-dir state-a \
  --body-file request-body.yaml --output request.yaml
python3 scripts/scp_wire.py receive --local implementer \
  --state-dir state-b --input request.yaml
```

The recipient now reads the validated `request.yaml` and performs its authorised work. To respond, use `scp_wire.py send --kind response --reply-to <request-id>` from `state-b`, then `receive` from `state-a`. These commands validate the **messages**, not execution of the task.

**If the recipient does not know HPX-SCP:** the sender must transfer a protocol bundle through its permitted channel:

```bash
python3 scripts/scp_wire.py bundle --output scp-protocol.zip
# If a 'need' was received, set NEED_MESSAGE_ID to its YAML id,
# then create an offer linked to that message:
python3 scripts/scp_wire.py offer --sender architect --recipient implementer \
  --conversation demo --reply-to "$NEED_MESSAGE_ID" \
  --bundle-ref scp-protocol.zip --output offer.yaml
# Send offer.yaml and scp-protocol.zip over the permitted channel.
# Receiver (with independently trusted verifier installed) stages the bundle:
python3 scripts/scp_wire.py inspect-bundle --input scp-protocol.zip \
  --stage-dir staged-protocol
```

Staging verifies consistency **without automatically activating** a new or mismatched protocol. Existing owner/repository trust policies still determine installation and compatibility. If the recipient lacks any trusted verifier, installation must happen through an authorised process before it can respond `ready`. The CLI is a file-based reference implementation, **not a network transport, an agent launcher or an identity-authentication system**.

## Human oversight without wasting context

`docs/engineering/semantic-protocol/PROTOCOL.md` has three parts: **canonical human-readable Markdown**, an appended machine-readable YAML projection, and an integrity manifest containing exactly two SHA-256 digests. A standalone verifier checks them *outside* the agent's context and rejects a mismatch or semantic divergence. Why? Agents need dependable shared rules without carrying the entire policy or its hashes in each prompt.

```bash
# Emit only the verified YAML rules and message contract needed to communicate:
python3 scripts/protocol_context.py --for negotiation
python3 scripts/protocol_context.py --for exchange --message-kind request
python3 scripts/protocol_context.py --for exchange --message-kind response
```

The compact bootstrap kernel governs identity, version, authority, validation and amendment. Repository `AGENTS.md` should point to the commands above, not paste the full specification into every session.

## Continuity and improvement

Agents must reverify protocol state and reload scoped YAML after recognised compaction or session resumption. Saved handoffs are working notes, not authority. Why? Summaries can discard governing details.

Agents may add **compatible** message kinds, optional fields and relationships when real communication needs arise. They update the canonical Markdown first, regenerate the YAML and both hashes, test the change and register it for all peers. **Breaking changes and changes to authority, security, the bootstrap kernel or human canonicality require owner approval.** Why? The communication language should improve through use without splitting into incompatible private variants.

## Where to look

- `docs/engineering/semantic-protocol/PROTOCOL.md` — authoritative rules, generated YAML and two-hash integrity manifest.
- `scripts/scp_wire.py` — discovery, readiness, protocol-bundle transfer and bidirectional YAML message checks.
- `scripts/protocol_context.py` — minimal verified YAML instructions for a task or message kind.
- `scripts/bootstrap_semantic_protocol.py` — fail-closed verification performed outside model context.
- `scripts/protocol_recovery.py` and `scripts/protocol_amendments.py` — continuity and controlled evolution.
- `AGENTS.md.fragment` — short instructions to merge into the repo's agent guidance.
- `tests/` — old-record compatibility, integrity, handshake, negotiation and exchange tests.

**Adoption:** This is a proposed repository kit, not an alteration to a live HPX checkout. Review it, merge the agent guidance without replacing existing project authority, and run `python3 -m unittest discover -s tests -p 'test_*.py'` before adoption.
