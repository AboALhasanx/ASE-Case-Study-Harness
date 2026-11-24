#!/usr/bin/env python3
"""Clone a target and record its exact revision without overwriting a study."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STUDIES = ROOT / "case-studies"


def validate_source(source: str, allow_local: bool) -> tuple[str, str]:
    if not source or any(ord(c) < 32 for c in source):
        raise ValueError("source must not contain control characters")
    try:
        parsed = urlsplit(source)
    except ValueError as exc:
        raise ValueError("invalid repository URL") from exc
    if parsed.scheme.lower() == "https":
        if not parsed.hostname or parsed.username is not None or parsed.password is not None:
            raise ValueError("HTTPS URL must have a host and must not contain credentials")
        if parsed.query or parsed.fragment or "\\" in source:
            raise ValueError("HTTPS URL must not contain a query, fragment, or backslash")
        if re.search(r"%(?![0-9a-fA-F]{2})", source):
            raise ValueError("invalid percent escape in URL")
        name = parsed.path.rstrip("/").rsplit("/", 1)[-1]
        if not name:
            raise ValueError("repository URL must include a repository name")
        return source, name
    if allow_local and not parsed.scheme:
        local = Path(source).expanduser().resolve(strict=True)
        if not local.is_dir():
            raise ValueError("local source must be a directory")
        return str(local), local.name
    # Windows drive letters parse as a scheme; support fixtures only when explicit.
    if allow_local and re.match(r"^[A-Za-z]:[\\/]", source):
        local = Path(source).expanduser().resolve(strict=True)
        if not local.is_dir():
            raise ValueError("local source must be a directory")
        return str(local), local.name
    raise ValueError("use a credential-free HTTPS repository URL (local paths require --allow-local)")


def git(args: list[str], cwd: Path | None = None) -> str:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="Never")
    try:
        result = subprocess.run(["git", *args], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                encoding="utf-8", errors="replace", timeout=180, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("Git could not start or timed out") from exc
    if result.returncode:
        # Git/network output may echo credentials or private URLs. Do not print it.
        raise RuntimeError(f"Git {args[0]} failed (exit {result.returncode}); verify access and repository URL")
    return result.stdout.strip()


def slug_for(name: str) -> str:
    if name.lower().endswith(".git"):
        name = name[:-4]
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:48].rstrip("-")
    return slug or "repository"


def license_evidence(repo: Path) -> str:
    # Treat a license filename as evidence only; do not infer its legal terms.
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.txt"):
        path = repo / name
        if path.is_file() and not path.is_symlink():
            return f"License file observed: `{name}`; inspect its contents to determine license."
    return "Not available: no standard license file found at the repository root."


def prepare(source: str, studies: Path, allow_local: bool = False) -> Path:
    source, name = validate_source(source, allow_local)
    studies = studies.expanduser().resolve()
    studies.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=".target-", dir=studies)).resolve()
    try:
        repo = temp / "target-repo"
        git(["clone", "--no-local", "--", source, str(repo)])
        sha = git(["rev-parse", "--verify", "HEAD^{commit}"], cwd=repo)
        if not re.fullmatch(r"[0-9a-f]{40,64}", sha):
            raise RuntimeError("Git returned an invalid commit identifier")
        try:
            branch = git(["symbolic-ref", "--quiet", "--short", "HEAD"], cwd=repo)
        except RuntimeError:
            branch = "detached HEAD (branch not available)"
        # Branch and source are untrusted data; normalize line endings for Markdown.
        branch = branch.replace("\r", " ").replace("\n", " ").replace("`", "'")
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        target = studies / f"{slug_for(name)}-{sha[:12]}"
        context = temp / "context"
        context.mkdir()
        manifest = (
            "# Target baseline\n\n"
            f"- Source URL: {source}\n"
            f"- Checkout branch: `{branch}`\n"
            f"- Commit: `{sha}`\n"
            f"- Captured UTC: `{timestamp}`\n"
            f"- License: {license_evidence(repo)}\n"
            "- Scope: Not yet determined; derive from repository evidence.\n"
            "- Retrieval: Local read-only clone; no target code executed.\n"
        )
        (context / "target-manifest.md").write_text(manifest, encoding="utf-8")
        # Reserve the final path atomically: another run cannot be replaced between
        # an existence check and rename, even on POSIX with an empty destination.
        try:
            target.mkdir()
        except FileExistsError as exc:
            raise FileExistsError("study destination already exists; existing work preserved") from exc
        marker = target / ".incomplete"
        marker.write_text("Baseline preparation in progress; inspect before resuming.\n", encoding="utf-8")
        # If interrupted, retain the reserved folder and its marker for inspection.
        (temp / "target-repo").rename(target / "target-repo")
        (temp / "context").rename(target / "context")
        marker.unlink()
        return target
    finally:
        if temp.exists():
            # Only delete the directory we created, directly inside the intended root.
            if temp.parent != studies or not temp.name.startswith(".target-") or temp.is_symlink():
                raise RuntimeError("refusing to remove unexpected temporary directory")
            def remove_readonly(function, path, exc_info):
                failed = Path(path).resolve()
                if temp not in failed.parents:
                    raise RuntimeError("refusing to modify path outside temporary directory")
                os.chmod(failed, stat.S_IWRITE | stat.S_IREAD)
                function(path)
            shutil.rmtree(temp, onerror=remove_readonly)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository_url", help="credential-free HTTPS repository URL")
    parser.add_argument("--studies", type=Path, default=DEFAULT_STUDIES, help="study destination root")
    parser.add_argument("--allow-local", action="store_true", help="allow local repository path (fixtures only)")
    args = parser.parse_args()
    try:
        path = prepare(args.repository_url, args.studies, args.allow_local)
    except OSError:
        # Filesystem errors can contain user-provided strings; do not echo them.
        print("Unable to prepare target: filesystem error or study already exists; existing work preserved", file=__import__("sys").stderr)
        return 2
    except (ValueError, RuntimeError) as exc:
        # Do not echo rejected input: it could contain a password or access token.
        print(f"Unable to prepare target: {exc}", file=__import__("sys").stderr)
        return 2
    print(f"Prepared target in {path}")
    print(f"Manifest: {path / 'context' / 'target-manifest.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
