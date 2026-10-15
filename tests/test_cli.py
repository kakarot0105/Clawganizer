"""CLI smoke tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from clawganizer.cli import main


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "2.1.0" in capsys.readouterr().out


def test_run_dry_run_empty_targets(tmp_path: Path, monkeypatch, capsys):
    home = tmp_path / "home"
    (home / "Downloads").mkdir(parents=True)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))

    with pytest.raises(SystemExit) as exc:
        main(["run", "--targets", "Downloads"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "Dry run" in out
    assert "Nothing to organize" in out


def test_workspace_create_list(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setenv("WORKSPACE", str(tmp_path / "oc"))
    with pytest.raises(SystemExit) as exc:
        main(["workspace", "create", "demo-app"])
    assert exc.value.code == 0
    with pytest.raises(SystemExit) as exc:
        main(["workspace", "list"])
    assert exc.value.code == 0
    assert "demo-app" in capsys.readouterr().out
