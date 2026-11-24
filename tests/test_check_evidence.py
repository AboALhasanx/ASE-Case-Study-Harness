import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check_evidence.py'
spec = importlib.util.spec_from_file_location('check_evidence', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

VALID = {
    'evidence': [{'id': 'E-01', 'source': 'README at commit abc, line 3'}],
    'claims': [
        {'id': 'C-01', 'claim': 'Setup is documented', 'status': 'Observed', 'evidence': ['E-01']},
        {'id': 'C-02', 'claim': 'Actual cost', 'status': 'Not Available', 'evidence': [], 'limitation': 'Records unavailable'},
        {'id': 'C-03', 'claim': 'Likely model', 'status': 'Inferred', 'evidence': ['E-01']},
        {'id': 'C-04', 'claim': 'Effort estimate', 'status': 'Estimated', 'evidence': ['E-01']},
    ],
    'deliverable_claims': ['C-01', 'C-02', 'C-03', 'C-04'],
}


class EvidenceCheckerTests(unittest.TestCase):
    def test_complete_ledger_passes(self):
        self.assertEqual(checker.check_ledger(VALID), [])

    def test_missing_evidence_and_missing_claim_reported(self):
        ledger = copy.deepcopy(VALID)
        ledger['claims'][0]['evidence'] = []
        ledger['claims'][2]['evidence'] = ['E-unknown']
        ledger['deliverable_claims'].append('C-missing')
        errors = '\n'.join(checker.check_ledger(ledger))
        self.assertIn('C-01 (Observed) needs at least one', errors)
        self.assertIn('unknown evidence id: E-unknown', errors)
        self.assertIn('unknown claim id: C-missing', errors)

    def test_duplicate_ids_and_absent_limitation_reported(self):
        ledger = copy.deepcopy(VALID)
        ledger['evidence'].append({'id': 'E-01', 'source': ''})
        ledger['claims'].append(copy.deepcopy(ledger['claims'][0]))
        ledger['claims'][1]['limitation'] = ''
        errors = '\n'.join(checker.check_ledger(ledger))
        for fragment in ['Duplicate evidence id', 'Duplicate claim id', 'non-empty source locator', 'needs a limitation']:
            self.assertIn(fragment, errors)

    def test_unexpected_json_shapes_fail_without_crashing(self):
        ledger = copy.deepcopy(VALID)
        ledger['claims'][0]['status'] = []
        ledger['claims'][0]['evidence'] = [{'id': 'E-01'}]
        ledger['deliverable_claims'] = ['C-01', 'C-01', None]
        errors = '\n'.join(checker.check_ledger(ledger))
        self.assertIn('invalid status', errors)
        self.assertIn('evidence must be an array', errors)
        self.assertIn('Duplicate deliverable claim', errors)
        self.assertIn('non-empty claim IDs', errors)

    def test_cli_status_for_pass_error_and_malformed_json(self):
        with tempfile.TemporaryDirectory() as dirname:
            path = Path(dirname) / 'ledger.json'
            path.write_text(json.dumps(VALID), encoding='utf-8')
            def run():
                return subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            good = run()
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertIn('does not verify', good.stdout)
            path.write_text('{"claims": []}', encoding='utf-8')
            self.assertEqual(run().returncode, 1)
            path.write_text('{bad', encoding='utf-8')
            self.assertEqual(run().returncode, 2)


if __name__ == '__main__':
    unittest.main()
