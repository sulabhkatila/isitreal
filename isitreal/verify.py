from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import httpx

from isitreal import cache
from isitreal.models import PackageResult
from isitreal.risk import compute_risk, get_fuzzy_suggestions
from isitreal.scanner import parse_dependencies, _risk_sort_key


def _get_package_downloads(name: str) -> Optional[int]:
    cache_key = f"pypistats:{name.lower()}"
    cached = cache.get_from_cache(cache_key)
    if cached is not None:
        return cached

    try:
        url = f"https://pypistats.org/api/packages/{name}/recent"
        response = httpx.get(url, timeout=5.0, follow_redirects=True)
        if response.status_code == 200:
            data = response.json()
            last_month = data.get("data", {}).get("last_month")
            if isinstance(last_month, int):
                cache.save_to_cache(cache_key, last_month)
                return last_month
    except Exception:
        # A failed pypistats lookup degrades cleanly without raising
        pass
    return None


def _parse_pypi_data(name: str, data: Dict[str, Any]) -> PackageResult:
    info = data.get("info", {})
    canonical_name = info.get("name", name)
    latest_version = info.get("version")
    summary = info.get("summary")

    releases = data.get("releases", {})
    total_releases = len(releases)

    earliest_dt: Optional[datetime] = None
    first_release_date: Optional[str] = None

    if isinstance(releases, dict):
        for ver, file_list in releases.items():
            if isinstance(file_list, list):
                for file_obj in file_list:
                    if isinstance(file_obj, dict):
                        iso_str = file_obj.get("upload_time_iso_8601")
                        if iso_str:
                            try:
                                dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
                                if dt.tzinfo is None:
                                    dt = dt.replace(tzinfo=timezone.utc)
                                if earliest_dt is None or dt < earliest_dt:
                                    earliest_dt = dt
                                    first_release_date = iso_str
                            except Exception:
                                pass

    age_days: Optional[int] = None
    if earliest_dt:
        now = datetime.now(timezone.utc)
        age_days = max(0, (now - earliest_dt).days)

    downloads = _get_package_downloads(name)
    risk, reasons = compute_risk(
        name=name,
        exists=True,
        age_days=age_days,
        downloads=downloads,
    )

    return PackageResult(
        name=name,
        exists=True,
        canonical_name=canonical_name,
        latest_version=latest_version,
        summary=summary,
        first_release_date=first_release_date,
        total_releases=total_releases,
        suggestions=[],
        risk=risk,
        reasons=reasons,
        age_days=age_days,
    )


def _make_missing_result(name: str, extra_reasons: Optional[List[str]] = None) -> PackageResult:
    risk, reasons = compute_risk(name=name, exists=False)
    if extra_reasons:
        reasons.extend(extra_reasons)
    return PackageResult(
        name=name,
        exists=False,
        suggestions=get_fuzzy_suggestions(name),
        risk=risk,
        reasons=reasons,
    )


def package(name: str) -> PackageResult:
    """Verify a single PyPI package name for existence and risk."""
    cache_key = f"pypi:{name.lower()}"
    cached = cache.get_from_cache(cache_key)
    if cached is not None:
        if isinstance(cached, dict):
            if not cached.get("exists", False):
                return _make_missing_result(name)
            data = cached.get("data", {})
            return _parse_pypi_data(name, data)

    url = f"https://pypi.org/pypi/{name}/json"
    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True)
        if response.status_code == 404:
            cache.save_to_cache(cache_key, {"exists": False})
            return _make_missing_result(name)
        elif response.status_code == 200:
            data = response.json()
            cache.save_to_cache(cache_key, {"exists": True, "data": data})
            return _parse_pypi_data(name, data)
        else:
            # Handle unexpected status codes gracefully
            return _make_missing_result(name, [f"PyPI registry returned status code {response.status_code}."])
    except Exception as e:
        # Never crash the check on network errors
        return _make_missing_result(name, [f"Network error communicating with PyPI: {str(e)}"])


def scan(target: str) -> List[PackageResult]:
    """Verify multiple dependencies from a file path or raw text."""
    names = parse_dependencies(target)
    results = [package(name) for name in names]
    results.sort(key=_risk_sort_key)
    return results
