# Preparing a target baseline

The user supplies a credential-free HTTPS Git repository URL. From the harness root run:

```text
python scripts/prepare_target.py https://github.com/pallets/flask.git
```

The helper clones into a temporary directory under `case-studies/`, records the checked-out branch, exact commit SHA, UTC timestamp, URL and a root license-file observation in `context/target-manifest.md`, and moves the complete result to `case-studies/<name>-<short-sha>/target-repo/`. It runs Git without a shell, does not intentionally execute target code, disables interactive prompts, and rejects credentials in URLs and existing destinations. Clone creates a local copy and contacts the remote; it is not a guarantee that network operations are read-only. A license filename is only evidence to inspect, not an identified license. Derive scope and audit findings separately.

Use `--studies <directory>` to set another output root. `--allow-local` permits local Git paths for offline fixtures; it is not needed for normal HTTPS use. Git must be installed and the repository accessible through existing read-only access. On a clone error the command reports the exit code without printing Git's raw output, which could expose credentials. It never asks for authentication or attempts to overwrite existing study work. This helper prepares a baseline; it does not perform the full case study or verify deliverables.

An interrupted process may leave a `.target-*` temporary folder or a reserved study directory with an `.incomplete` marker under the selected output root. If interruption occurs between reserving the directory and writing the marker, the directory may be empty. New runs create their own unique temporary folder; they neither reuse nor delete a previous interrupted folder. Inspect any leftover before removing it. A study with `.incomplete` or a missing checkout/manifest must not be treated as a completed baseline; check it and recover or recreate it deliberately.

If the same repository revision was already prepared, the helper returns an error and preserves all existing work. The agent can check for `.incomplete`, inspect the existing `context/target-manifest.md`, confirm its URL and commit against the checkout, and resume a complete study rather than overwrite it. The helper does not automatically resume or verify existing work.
