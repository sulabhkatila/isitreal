from typing import List
from mcp.server.fastmcp import FastMCP

from slopguard import verify
from slopguard.models import PackageResult

mcp = FastMCP(
    "slopguard",
    instructions="Dependency reality-checker for AI coding agents. Call before adding dependencies or installing packages.",
)


@mcp.tool()
def verify_package(name: str, ecosystem: str = "pypi") -> PackageResult:
    """Call this before adding any new package to a project or running pip install, to confirm the package is real and not a known hallucination/typosquat risk.

    Args:
        name: The name of the package to verify.
        ecosystem: The package repository ecosystem (v1 supports 'pypi').
    """
    if ecosystem.lower() != "pypi":
        res = verify.package(name)
        if not res.reasons:
            res.reasons = []
        res.reasons.append(f"Note: Verified against PyPI registry (ecosystem '{ecosystem}' fallback in v1).")
        return res
    return verify.package(name)


@mcp.tool()
def verify_dependencies(file_contents: str) -> List[PackageResult]:
    """Call this before adding any new package to a project or running pip install, to confirm the package is real and not a known hallucination/typosquat risk.
    Scans a requirements.txt, pyproject.toml, or raw list of dependencies and verifies every package.

    Args:
        file_contents: The raw text contents of a requirements.txt file, pyproject.toml file, or multi-line dependency list.
    """
    return verify.scan(file_contents)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
