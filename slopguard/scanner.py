import os
import re
from pathlib import Path
from typing import List, Set, Optional
from packaging.requirements import Requirement

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore
    except ImportError:
        tomllib = None  # type: ignore


def _extract_name_from_req_line(line: str) -> Optional[str]:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("-") or line.startswith("--"):
        return None
    # strip inline comments
    if " #" in line:
        line = line.split(" #", 1)[0].strip()
    try:
        req = Requirement(line)
        return req.name
    except Exception:
        # Fallback regex for raw package names or simple strings
        match = re.match(r"^[a-zA-Z0-9][-a-zA-Z0-9_.]*", line)
        if match:
            return match.group(0)
    return None


def _parse_toml_content(content: str) -> List[str]:
    if not tomllib:
        return []
    try:
        data = tomllib.loads(content)
    except Exception:
        return []

    deps: List[str] = []
    # PEP 621 [project] dependencies
    project = data.get("project", {})
    if isinstance(project, dict):
        for dep in project.get("dependencies", []):
            if isinstance(dep, str):
                deps.append(dep)
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, dict):
            for group_deps in optional.values():
                if isinstance(group_deps, list):
                    for dep in group_deps:
                        if isinstance(dep, str):
                            deps.append(dep)

    # Poetry dependencies
    tool = data.get("tool", {})
    if isinstance(tool, dict):
        poetry = tool.get("poetry", {})
        if isinstance(poetry, dict):
            p_deps = poetry.get("dependencies", {})
            if isinstance(p_deps, dict):
                for name in p_deps.keys():
                    if name.lower() != "python":
                        deps.append(name)
            p_dev = poetry.get("dev-dependencies", {})
            if isinstance(p_dev, dict):
                for name in p_dev.keys():
                    deps.append(name)

    names: List[str] = []
    for line in deps:
        name = _extract_name_from_req_line(line)
        if name:
            names.append(name)
    return names


def _parse_requirements_content(content: str) -> List[str]:
    names: List[str] = []
    for line in content.splitlines():
        name = _extract_name_from_req_line(line)
        if name:
            names.append(name)
    return names


def parse_dependencies(target: str) -> List[str]:
    """Parse unique package names from a file path or raw text content."""
    content: str
    is_toml = False

    # Check if target is a file path
    if os.path.exists(target) and os.path.isfile(target):
        try:
            with open(target, "r", encoding="utf-8") as f:
                content = f.read()
            if str(target).lower().endswith(".toml"):
                is_toml = True
        except Exception:
            return []
    else:
        content = target
        # Check if raw text looks like TOML
        if "[project]" in content or "dependencies =" in content:
            is_toml = True

    names: List[str] = []
    if is_toml:
        names = _parse_toml_content(content)
        if not names:
            # Fallback to lines if TOML parsing yielded nothing
            names = _parse_requirements_content(content)
    else:
        names = _parse_requirements_content(content)

    # Deduplicate while preserving order
    seen: Set[str] = set()
    unique_names: List[str] = []
    for name in names:
        lower_name = name.lower()
        if lower_name not in seen:
            seen.add(lower_name)
            unique_names.append(name)
    return unique_names


def _risk_sort_key(res) -> tuple:
    # Worst risk first: "high" -> exists=False (None) -> "unknown" -> "low"
    risk_rank = {
        "high": 0,
        "unknown": 2,
        "low": 3,
    }
    if res.risk == "high":
        rank = 0
    elif not res.exists:
        rank = 1
    else:
        rank = risk_rank.get(res.risk, 2)
    return (rank, res.name.lower())
