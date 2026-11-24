#!/usr/bin/env python3
"""Check structural traceability of a JSON evidence ledger; not factual truth."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

STATUSES = {'Observed', 'Inferred', 'Estimated', 'Not Available'}


def check_ledger(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ['Ledger must be a JSON object.']
    evidence = data.get('evidence')
    claims = data.get('claims')
    deliverables = data.get('deliverable_claims')
    if not isinstance(evidence, list):
        errors.append('evidence must be an array.'); evidence = []
    if not isinstance(claims, list) or not claims:
        errors.append('claims must be a non-empty array.'); claims = []
    if not isinstance(deliverables, list) or not deliverables:
        errors.append('deliverable_claims must be a non-empty array.'); deliverables = []
    evidence_ids: set[str] = set()
    claim_ids: set[str] = set()
    for idx, item in enumerate(evidence, 1):
        if not isinstance(item, dict):
            errors.append(f'evidence[{idx}] must be an object.'); continue
        eid = item.get('id')
        if not isinstance(eid, str) or not eid.strip():
            errors.append(f'evidence[{idx}] needs a non-empty id.'); continue
        if eid != eid.strip():
            errors.append(f'evidence id {eid!r} must not have surrounding whitespace.')
        if eid in evidence_ids:
            errors.append(f'Duplicate evidence id: {eid}.')
        evidence_ids.add(eid)
        if not isinstance(item.get('source'), str) or not item['source'].strip():
            errors.append(f'Evidence {eid} needs a non-empty source locator.')
    for idx, item in enumerate(claims, 1):
        if not isinstance(item, dict):
            errors.append(f'claims[{idx}] must be an object.'); continue
        cid = item.get('id')
        if not isinstance(cid, str) or not cid.strip():
            errors.append(f'claims[{idx}] needs a non-empty id.'); continue
        if cid != cid.strip():
            errors.append(f'claim id {cid!r} must not have surrounding whitespace.')
        if cid in claim_ids:
            errors.append(f'Duplicate claim id: {cid}.')
        claim_ids.add(cid)
        if not isinstance(item.get('claim'), str) or not item['claim'].strip():
            errors.append(f'Claim {cid} needs non-empty claim text.')
        status = item.get('status')
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f'Claim {cid} has invalid status: {status!r}.')
        refs = item.get('evidence')
        if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref.strip() for ref in refs):
            errors.append(f'Claim {cid} evidence must be an array of non-empty evidence IDs.'); refs = []
        if isinstance(status, str) and status in {'Observed', 'Inferred', 'Estimated'} and not refs:
            errors.append(f'Claim {cid} ({status}) needs at least one evidence reference.')
        if status == 'Not Available' and (not isinstance(item.get('limitation'), str) or not item['limitation'].strip()):
            errors.append(f'Claim {cid} (Not Available) needs a limitation.')
        for ref in refs:
            if ref not in evidence_ids:
                errors.append(f'Claim {cid} references unknown evidence id: {ref}.')
    seen_deliverables: set[str] = set()
    for ref in deliverables:
        if not isinstance(ref, str) or not ref.strip():
            errors.append('deliverable_claims must contain non-empty claim IDs.'); continue
        if ref in seen_deliverables:
            errors.append(f'Duplicate deliverable claim id: {ref}.')
        seen_deliverables.add(ref)
        if ref not in claim_ids:
            errors.append(f'Deliverable references unknown claim id: {ref}.')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path, help='JSON ledger file')
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding='utf-8-sig'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f'Cannot read ledger: {exc}', file=sys.stderr)
        return 2
    errors = check_ledger(data)
    if errors:
        for error in errors:
            print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print('Ledger structure and listed references pass. This does not verify the sources, their support, or the completeness of the supplied claim list.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
