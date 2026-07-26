import difflib
import json
import re
from pathlib import Path
from typing import Optional, Set, Tuple, List

_TOP_PACKAGES: Optional[Set[str]] = None
_HALLUCINATED_PACKAGES: Optional[Set[str]] = None


def _get_data_dir() -> Path:
    return Path(__file__).parent / "data"


def load_top_packages() -> Set[str]:
    global _TOP_PACKAGES
    if _TOP_PACKAGES is None:
        path = _get_data_dir() / "top_pypi_packages.json"
        try:
            with open(path, "r", encoding="utf-8") as f:
                _TOP_PACKAGES = set(json.load(f))
        except Exception:
            _TOP_PACKAGES = set()
    return _TOP_PACKAGES


def load_hallucinated_packages() -> Set[str]:
    global _HALLUCINATED_PACKAGES
    if _HALLUCINATED_PACKAGES is None:
        path = _get_data_dir() / "hallucinated_packages.json"
        try:
            with open(path, "r", encoding="utf-8") as f:
                _HALLUCINATED_PACKAGES = set(json.load(f))
        except Exception:
            _HALLUCINATED_PACKAGES = set()
    return _HALLUCINATED_PACKAGES


def get_fuzzy_suggestions(name: str, limit: int = 3) -> List[str]:
    top = load_top_packages()
    if not top:
        return []
    matches = difflib.get_close_matches(name.lower(), list(top), n=limit, cutoff=0.6)
    return matches


def check_conflation(name: str, top_packages: Set[str]) -> Tuple[bool, Optional[str]]:
    lower = name.lower()
    if lower in top_packages:
        return False, None

    # Check hyphen or underscore separated parts
    parts = re.split(r"[-_]", lower)
    if len(parts) >= 2:
        matching_parts = [p for p in parts if len(p) >= 3 and p in top_packages]
        if len(matching_parts) >= 2:
            return True, f"Package name looks like a conflation of well-known packages ('{matching_parts[0]}' and '{matching_parts[1]}')."

    # Check unseparated substring concatenation (e.g. jscodeshiftreact)
    if len(lower) >= 8:
        for i in range(4, len(lower) - 3):
            left = lower[:i]
            right = lower[i:]
            if left in top_packages and right in top_packages:
                return True, f"Package name looks like a conflation of well-known packages ('{left}' and '{right}')."

    return False, None


def compute_risk(
    name: str,
    exists: bool,
    age_days: Optional[int] = None,
    downloads: Optional[int] = None,
) -> Tuple[Optional[str], List[str]]:
    lower = name.lower()
    hallucinated = load_hallucinated_packages()
    top_packages = load_top_packages()
    reasons: List[str] = []

    # 1. Automatic high risk if in hallucinated list
    if lower in hallucinated:
        reasons.append("Package name is in the known list of AI-hallucinated/slopsquatted packages.")
        return "high", reasons

    # 2. Check for conflation of well-known packages
    is_conf, conf_reason = check_conflation(name, top_packages)
    if is_conf and conf_reason:
        reasons.append(conf_reason)
        # Any conflation that is not itself a top package is flagged as high risk
        return "high", reasons

    if not exists:
        return None, []

    # 3. Top packages list
    if lower in top_packages:
        reasons.append("Package is in the top PyPI packages by download count.")
        if age_days is not None:
            reasons.append(f"Package has been published for {age_days} days.")
        return "low", reasons

    # 4. Age and download signals for packages not in top 5000
    if age_days is not None:
        reasons.append(f"Package has been published for {age_days} days.")
        if age_days < 30:
            reasons.append("Package was first published less than 30 days ago.")
            return "high", reasons
        elif age_days >= 365:
            if downloads is not None and downloads >= 500:
                reasons.append(f"Package has {downloads:,} recent downloads.")
                return "low", reasons
            elif downloads is None:
                return "low", reasons

    # Default fallback when signals are uncertain or lookup degraded
    if not reasons:
        reasons.append("Package is not in top packages and lacks strong safety signals.")
    return "unknown", reasons
