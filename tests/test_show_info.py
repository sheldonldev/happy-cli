from typer.testing import CliRunner

from happy_cli import app


def test_show_info():
    runner = CliRunner()
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "version" in result.stdout


if __name__ == '__main__':
    test_show_info()
