from depcheck.risk import (
    check_conflation,
    compute_risk,
    get_fuzzy_suggestions,
    load_hallucinated_packages,
    load_top_packages,
)


def test_load_static_data():
    top = load_top_packages()
    hallucinated = load_hallucinated_packages()
    assert "requests" in top
    assert "react-codeshift" in hallucinated


def test_get_fuzzy_suggestions():
    sugg = get_fuzzy_suggestions("fancylib")
    assert "fancy-lib" in sugg


def test_check_conflation():
    top = load_top_packages()
    # Conflation with separator
    is_conf, reason = check_conflation("requests-pydantic", top)
    assert is_conf is True
    assert "conflation" in (reason or "")

    # Normal top package is not a conflation
    is_conf, reason = check_conflation("requests", top)
    assert is_conf is False


def test_compute_risk_hallucinated():
    risk, reasons = compute_risk("react-codeshift", exists=False)
    assert risk == "high"
    assert any("hallucinated" in r for r in reasons)


def test_compute_risk_conflation_new():
    risk, reasons = compute_risk("requests-pydantic", exists=True, age_days=10, downloads=100)
    assert risk == "high"
    assert any("conflation" in r for r in reasons)


def test_compute_risk_very_new_package():
    risk, reasons = compute_risk("brandnewpkg999", exists=True, age_days=15, downloads=50)
    assert risk == "high"
    assert any("less than 30 days" in r for r in reasons)


def test_compute_risk_low_risk_established():
    risk, reasons = compute_risk("requests", exists=True, age_days=4000, downloads=100000)
    assert risk == "low"
    assert any("top PyPI packages" in r for r in reasons)


def test_compute_risk_unknown():
    risk, reasons = compute_risk("someobscurepkg111", exists=True, age_days=60, downloads=None)
    assert risk == "unknown"
