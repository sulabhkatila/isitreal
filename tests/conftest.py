import pytest
import respx
from httpx import Response
from isitreal import cache


@pytest.fixture(autouse=True)
def isolated_cache(tmp_path, monkeypatch):
    """Use an isolated temporary cache directory for every test."""
    monkeypatch.setenv("ISITREAL_CACHE_DIR", str(tmp_path / "cache"))
    cache.clear_cache()
    yield
    cache.clear_cache()


@pytest.fixture
def mock_pypi():
    """Mock PyPI and pypistats network responses for standard test packages."""
    with respx.mock(assert_all_called=False) as respx_mock:
        # Mock requests package (200 OK)
        respx_mock.get("https://pypi.org/pypi/requests/json").mock(
            return_value=Response(
                200,
                json={
                    "info": {
                        "name": "requests",
                        "version": "2.31.0",
                        "summary": "Python HTTP for Humans.",
                    },
                    "releases": {
                        "0.1.0": [
                            {"upload_time_iso_8601": "2011-02-14T08:49:42.641660Z"}
                        ]
                    },
                },
            )
        )
        respx_mock.get("https://pypistats.org/api/packages/requests/recent").mock(
            return_value=Response(
                200,
                json={"data": {"last_month": 50000000}},
            )
        )

        # Mock react-codeshift (404 Not Found on PyPI)
        respx_mock.get("https://pypi.org/pypi/react-codeshift/json").mock(
            return_value=Response(404)
        )

        # Mock fancylib (404 Not Found on PyPI)
        respx_mock.get("https://pypi.org/pypi/fancylib/json").mock(
            return_value=Response(404)
        )

        # Mock thispackagedoesnotexist12345 (404 Not Found on PyPI)
        respx_mock.get("https://pypi.org/pypi/thispackagedoesnotexist12345/json").mock(
            return_value=Response(404)
        )

        yield respx_mock
