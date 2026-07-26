from slopguard import verify
from slopguard.scanner import parse_dependencies


def test_parse_requirements_txt(tmp_path):
    content = """
    # Comment line
    -r requirements-dev.txt
    requests>=2.31.0 # HTTP library
    react-codeshift==1.0.0
    requests  # Duplicate should be removed
    --index-url https://pypi.org/simple
    fancylib
    """
    req_file = tmp_path / "requirements.txt"
    req_file.write_text(content, encoding="utf-8")

    names = parse_dependencies(str(req_file))
    assert names == ["requests", "react-codeshift", "fancylib"]


def test_parse_pyproject_toml(tmp_path):
    content = """
    [project]
    name = "example"
    dependencies = [
        "requests>=2.0.0",
        "react-codeshift",
    ]

    [project.optional-dependencies]
    dev = ["pytest>=8.0.0"]
    """
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(content, encoding="utf-8")

    names = parse_dependencies(str(toml_file))
    assert set(names) == {"requests", "react-codeshift", "pytest"}


def test_parse_raw_text():
    raw = "requests>=2.31.0\nreact-codeshift"
    names = parse_dependencies(raw)
    assert names == ["requests", "react-codeshift"]


def test_verify_scan_sorting(mock_pypi):
    results = verify.scan("requests>=2.31.0\nreact-codeshift\nfancylib")
    assert len(results) == 3
    # Worst risk first: react-codeshift (high risk) should be first
    assert results[0].name == "react-codeshift"
    assert results[0].risk == "high"
    # requests (low risk) should come last
    assert results[-1].name == "requests"
    assert results[-1].risk == "low"
