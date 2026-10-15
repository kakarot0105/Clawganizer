"""Tests for whole-computer organization."""

from __future__ import annotations

import json
from pathlib import Path

import clawganizer.config as config_mod
from clawganizer.organizer import organize, plan_moves, undo_last_run


def _cfg(tmp_path: Path, targets: dict[str, bool] | None = None) -> dict:
    base = config_mod.load_default_config()
    base["destination_root"] = str(tmp_path / "home")
    base["targets"] = targets or {"Downloads": True, "Desktop": True, "Documents": False}
    return base


def test_plan_moves_by_extension(tmp_path: Path, monkeypatch):
    home = tmp_path / "home"
    downloads = home / "Downloads"
    desktop = home / "Desktop"
    downloads.mkdir(parents=True)
    desktop.mkdir(parents=True)

    (downloads / "photo.JPG").write_text("img")
    (downloads / "notes.pdf").write_text("pdf")
    (downloads / "song.mp3").write_text("audio")
    (desktop / "Screenshot 2026-01-01.png").write_text("shot")
    (downloads / "project").mkdir()  # directories are left alone
    (downloads / ".secret").write_text("hidden")

    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))

    cfg = _cfg(tmp_path)
    planned = plan_moves(cfg)
    sources = {Path(m.source).name for m in planned}
    assert sources == {"photo.JPG", "notes.pdf", "song.mp3", "Screenshot 2026-01-01.png"}
    categories = {m.category for m in planned}
    assert "Images" in categories
    assert "Documents" in categories
    assert "Audio" in categories
    assert "Screenshots" in categories


def test_organize_apply_and_undo(tmp_path: Path, monkeypatch):
    home = tmp_path / "home"
    downloads = home / "Downloads"
    downloads.mkdir(parents=True)
    src = downloads / "report.pdf"
    src.write_text("hello")

    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.setattr(config_mod, "LOG_DIR", tmp_path / "logs")
    # organizer imports LOG_DIR at module level — patch there too
    import clawganizer.organizer as organizer_mod

    monkeypatch.setattr(organizer_mod, "LOG_DIR", tmp_path / "logs")

    cfg = _cfg(tmp_path)
    dry = organize(dry_run=True, config=cfg)
    assert dry.move_count == 1
    assert src.exists()

    applied = organize(dry_run=False, config=cfg)
    assert applied.move_count == 1
    assert not src.exists()
    dest = Path(applied.moved[0].destination)
    assert dest.exists()
    assert dest.read_text() == "hello"

    undone = undo_last_run(dry_run=False)
    assert undone.move_count == 1
    assert src.exists()
    assert src.read_text() == "hello"


def test_name_collision(tmp_path: Path, monkeypatch):
    home = tmp_path / "home"
    downloads = home / "Downloads"
    dest_dir = home / "Documents" / "Organized"
    downloads.mkdir(parents=True)
    dest_dir.mkdir(parents=True)
    (downloads / "notes.pdf").write_text("new")
    (dest_dir / "notes.pdf").write_text("old")

    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    import clawganizer.organizer as organizer_mod

    monkeypatch.setattr(organizer_mod, "LOG_DIR", tmp_path / "logs")

    cfg = _cfg(tmp_path)
    result = organize(dry_run=False, config=cfg)
    assert result.move_count == 1
    assert Path(result.moved[0].destination).name == "notes_1.pdf"


def test_custom_source_path(tmp_path: Path, monkeypatch):
    clutter = tmp_path / "clutter"
    clutter.mkdir()
    (clutter / "clip.mp4").write_text("vid")

    import clawganizer.organizer as organizer_mod

    monkeypatch.setattr(organizer_mod, "LOG_DIR", tmp_path / "logs")

    cfg = _cfg(tmp_path)
    result = organize(dry_run=False, config=cfg, sources=[clutter])
    assert result.move_count == 1
    assert "Videos" == result.moved[0].category
    assert json.loads(Path(result.log_path).read_text())["dry_run"] is False
