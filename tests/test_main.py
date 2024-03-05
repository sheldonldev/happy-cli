from typer.testing import CliRunner

from jampy_cli import app

runner = CliRunner()


def test_info():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "version" in result.stdout.lower()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "usage" in result.stdout.lower()

    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0
    assert "usage" in result.stdout.lower()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.stdout.lower()

    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert "version" in result.stdout.lower()
