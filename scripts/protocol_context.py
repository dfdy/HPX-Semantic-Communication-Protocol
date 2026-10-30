#!/usr/bin/env python3
"""Emit minimal *verified* semantic-only context after fail-closed canonical preflight.

Example: python3 scripts/protocol_context.py --for implement --for records --record-type implementation_evidence
This process reads natural language solely for verification; stdout contains no source prose.
"""
from __future__ import annotations
import argparse
import json
import sys

from bootstrap_semantic_protocol import yaml_bytes
from pathlib import Path
from bootstrap_semantic_protocol import PROTOCOL, SCOPES, BootstrapError, verify_path
from protocol_amendments import validate_registry


def packet_for(projection: dict, scopes: list[str], record_types: list[str] | None = None,
               relations: list[str] | None = None) -> dict:
    requested = set(scopes) | {'kernel', 'baseline'}
    if not requested <= SCOPES:
        raise BootstrapError('unknown requested context scope: ' + ','.join(sorted(requested - SCOPES)))
    type_map = {x['kind']:x for x in projection['record_types']}
    relation_map = {x['name']:x for x in projection['relationship_types']}
    for kind in record_types or []:
        if kind not in type_map:
            raise BootstrapError('unknown record kind: ' + kind)
    for relation in relations or []:
        if relation not in relation_map:
            raise BootstrapError('unknown relation: ' + relation)
    if record_types and 'records' not in requested:
        requested.add('records')
    if relations and 'records' not in requested:
        requested.add('records')
    packet = {
        'protocol': 'HPX-SCP',
        'version': projection['protocol_version'],
        'verified': True,
        'scopes': sorted(requested),
        'rules': [{'id': r['id'], 'do': r['directive']} for r in projection['rules'] if r['scope'] in requested],
    }
    if record_types:
        packet['record_contracts'] = [type_map[k] for k in dict.fromkeys(record_types)]
    if relations:
        packet['relations'] = [relation_map[r] for r in dict.fromkeys(relations)]
    return packet


def scoped_packet_as_yaml(packet: dict, projection: dict) -> str:
    scope_lookup = {r['id']: r['scope'] for r in projection['rules']}
    grouped = {scope: {} for scope in packet['scopes']}
    for rule in packet['rules']:
        grouped[scope_lookup[rule['id']]][rule['id']] = rule['do']
    payload = {'HPX-SCP': {'version':packet['version'], 'verified':True, 'scopes':grouped}}
    if 'record_contracts' in packet:
        payload['HPX-SCP']['records'] = {r['kind']:{'statuses':r['statuses'],
            'required':r['required_content_fields'],'meaning':r['meaning']} for r in packet['record_contracts']}
    if 'relations' in packet:
        payload['HPX-SCP']['relationships'] = {r['name']:r['meaning'] for r in packet['relations']}
    return yaml_bytes(payload).decode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--protocol', type=Path, default=PROTOCOL)
    parser.add_argument('--for', dest='scopes', action='append', default=[], choices=sorted(SCOPES))
    parser.add_argument('--record-type', action='append', default=[])
    parser.add_argument('--relation', action='append', default=[])
    parser.add_argument('--trusted-sha256')
    parser.add_argument('--format', choices=('yaml','json'), default='yaml')
    args = parser.parse_args()
    try:
        verified = verify_path(args.protocol, args.trusted_sha256)
        validate_registry(verified, root=args.protocol.resolve().parents[3] if args.protocol.resolve() == PROTOCOL.resolve() else None)
        result = packet_for(verified, args.scopes, args.record_type, args.relation)
    except (BootstrapError, OSError) as exc:
        print('CONTEXT REFUSED: ' + str(exc), file=sys.stderr)
        return 1
    if args.format == 'yaml':
        print(scoped_packet_as_yaml(result, verified), end='')
    else:
        print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
