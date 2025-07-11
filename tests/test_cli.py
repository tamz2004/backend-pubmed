import subprocess

def test_cli_runs():
    result = subprocess.run(
        ["python", "-m", "poetry", "run", "get-papers-list", "covid", "-d"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
