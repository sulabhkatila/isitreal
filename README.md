# depcheck

**Dependency reality-checker for AI coding agents — verify before install, not scan after the fact.**

---

## Context (Why This Exists)

AI coding agents frequently hallucinate package names — inventing plausible but nonexistent dependencies, or conflating two real packages into a fake one (e.g. `jscodeshift` + `react-codemod` → `react-codeshift`). Attackers pre-register these hallucinated names with malicious payloads ("slopsquatting"), so an agent that installs a dependency without verifying it first can pull in attacker-controlled code.

`depcheck` closes that gap: it lets an AI coding agent check, in one call, whether a package name is real, safe, and well-established — **before** adding it to a project or running `pip install`.

---

## Features

1. **Existence Verification**: Queries live PyPI registry data with automatic on-disk caching (`24h` TTL by default) to prevent rate limits.
2. **Fuzzy Suggestions**: Provides up to 3 close-match alternatives against a bundled local list of top ~5,000 PyPI packages when a package doesn't exist.
3. **Risk Scoring**:
   - Flags automatic `"high"` risk for known AI-hallucinated/slopsquatted names (seeded from security research, e.g. `react-codeshift`, `django-postgres`).
   - Detects conflated package names (e.g. merging two well-known packages into one).
   - Computes risk based on package age (`age_days`), download statistics from `pypistats`, and membership in top PyPI downloads.
   - Degrades gracefully on network errors (`"unknown"` risk) without failing checks.
4. **Batch & Scan Mode**: Scans `requirements.txt`, `pyproject.toml`, or raw text dependencies and returns structured results sorted **worst-risk-first**.

---

## Installation

Install from PyPI (or locally from source):

```bash
pip install depcheck
```

For development and running tests:

```bash
pip install -e '.[dev]'
pytest
```

---

## Interfaces

`depcheck` exposes three distinct interfaces in priority order:

### 1. Python API

```python
from depcheck import verify

# Verify a nonexistent package
res = verify.package("fancylib")
# -> PackageResult(name='fancylib', exists=False, suggestions=['fancy-lib', ...], risk=None, ...)

# Verify a well-established package
res = verify.package("requests")
# -> PackageResult(name='requests', exists=True, risk='low', age_days=5640, ...)

# Verify a known hallucinated/slopsquatted package
res = verify.package("react-codeshift")
# -> PackageResult(name='react-codeshift', exists=False, risk='high', reasons=['Package name is in the known list of AI-hallucinated/slopsquatted packages.'])

# Scan a requirements.txt or pyproject.toml file
results = verify.scan("requirements.txt")
# -> list[PackageResult] sorted worst-risk-first
```

#### `PackageResult` Fields
- `name` (`str`): The queried package name.
- `exists` (`bool`): Whether the package exists on PyPI.
- `canonical_name` (`str | None`): Canonical package name from PyPI.
- `latest_version` (`str | None`): Latest published version.
- `summary` (`str | None`): Short package description from PyPI metadata.
- `first_release_date` (`str | None`): ISO-8601 timestamp of the package's earliest release.
- `total_releases` (`int`): Number of published releases.
- `suggestions` (`list[str]`): Suggested package alternatives if `exists=False`.
- `risk` (`str | None`): Risk level — `"low"`, `"unknown"`, or `"high"`, or `None` for typical nonexistent packages.
- `reasons` (`list[str]`): Explainable reasons for the risk classification.
- `age_days` (`int | None`): Age of the package in days since its first release.

---

### 2. Command Line Interface (CLI)

Verify a single package:
```bash
depcheck check fancylib
depcheck check requests
```

Scan a dependency file (`requirements.txt` or `pyproject.toml`):
```bash
depcheck scan requirements.txt
```

Fail in CI pipelines if any package is high risk:
```bash
depcheck scan requirements.txt --fail-on high
depcheck check react-codeshift --fail-on high
```
*(Exits with nonzero code `1` when a matching or higher risk threshold is encountered.)*

---

### 3. Model Context Protocol (MCP) Server

`depcheck` includes a native Model Context Protocol (MCP) server built with the official Python `mcp` SDK (`FastMCP`), exposing two tools:

- `verify_package(name: str, ecosystem: str = "pypi") -> PackageResult`
- `verify_dependencies(file_contents: str) -> list[PackageResult]`

#### Registering in Claude Code / Claude Desktop / AI Agents

You can run the server via either `depcheck-mcp` or `depcheck mcp`.

Add the server to your Claude Desktop configuration (`~/.config/Claude/claude_desktop_config.json` on macOS/Linux or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "depcheck": {
      "command": "depcheck-mcp"
    }
  }
}
```

Or configure it in your Claude Code project (`.claude.json`):

```json
{
  "mcpServers": {
    "depcheck": {
      "command": "depcheck-mcp",
      "args": []
    }
  }
}
```

When configured, AI coding agents should call `verify_package` or `verify_dependencies` **before** writing requirements files or executing `pip install`, ensuring every dependency is genuine and safe.

---

## License

MIT
