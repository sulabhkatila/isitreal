import pytest
import respx
from httpx import Response, ConnectError
from depcheck import verify


def test_verify_requests_package(mock_pypi):
    res = verify.package("requests")
    assert res.exists is True
    assert res.risk == "low"
    assert res.canonical_name == "requests"
    assert res.latest_version == "2.31.0"
    assert res.age_days is not None and res.age_days > 4000
    assert "Package is in the top PyPI packages by download count." in res.reasons


def test_verify_react_codeshift(mock_pypi):
    res = verify.package("react-codeshift")
    assert res.exists is False
    assert res.risk == "high"
    assert any("hallucinated" in r for r in res.reasons)


def test_verify_nonexistent_package(mock_pypi):
    res = verify.package("thispackagedoesnotexist12345")
    assert res.exists is False
    assert res.risk is None
    assert res.suggestions == []


def test_verify_fancylib_suggestions(mock_pypi):
    res = verify.package("fancylib")
    assert res.exists is False
    assert res.risk is None
    assert "fancy-lib" in res.suggestions


def test_pypistats_failure_degrades_gracefully():
    with respx.mock() as respx_mock:
        respx_mock.get("https://pypi.org/pypi/custompkg123/json").mock(
            return_value=Response(
                200,
                json={
                    "info": {"name": "custompkg123", "version": "1.0.0"},
                    "releases": {},
                },
            )
        )
        respx_mock.get("https://pypistats.org/api/packages/custompkg123/recent").mock(
            return_value=Response(500)
        )

        res = verify.package("custompkg123")
        assert res.exists is True
        # Without stats or top-package signal, risk defaults to unknown
        assert res.risk == "unknown"


def test_network_error_degrades_gracefully():
    with respx.mock() as respx_mock:
        respx_mock.get("https://pypi.org/pypi/networkerrpkg/json").mock(
            side_effect=ConnectError("Connection refused")
        )

        res = verify.package("networkerrpkg")
        assert res.exists is False
        assert any("Network error" in r for r in res.reasons)
