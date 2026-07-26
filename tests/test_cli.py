from click.testing import CliRunner
from slopguard.cli import cli


def test_cli_check_requests(mock_pypi):
    runner = CliRunner()
    result = runner.invoke(cli, ["check", "requests"])
    assert result.exit_code == 0
    assert "requests" in result.output
    assert "LOW" in result.output


def test_cli_check_react_codeshift_fail_on(mock_pypi):
    runner = CliRunner()
    result = runner.invoke(cli, ["check", "react-codeshift", "--fail-on", "high"])
    assert result.exit_code == 1
    assert "react-codeshift" in result.output
    assert "HIGH" in result.output


def test_cli_scan_fail_on_high(tmp_path, mock_pypi):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("requests>=2.31.0\nreact-codeshift\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(cli, ["scan", str(req_file), "--fail-on", "high"])
    assert result.exit_code == 1
    assert "react-codeshift" in result.output
    assert "requests" in result.output


def test_cli_scan_clean(tmp_path, mock_pypi):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("requests>=2.31.0\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(cli, ["scan", str(req_file), "--fail-on", "high"])
    assert result.exit_code == 0
    assert "requests" in result.output
