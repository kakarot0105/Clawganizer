"""UI HTTP API tests."""

from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from clawganizer.ui.server import ClawganizerHandler, ThreadingHTTPServer


@pytest.fixture()
def ui_server(tmp_path, monkeypatch):
    home = tmp_path / "home"
    downloads = home / "Downloads"
    downloads.mkdir(parents=True)
    (downloads / "shot.pdf").write_text("x")

    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))

    import clawganizer.config as config_mod
    import clawganizer.organizer as organizer_mod
    import clawganizer.ui.server as ui_server_mod

    monkeypatch.setattr(organizer_mod, "LOG_DIR", tmp_path / "logs")
    monkeypatch.setattr(config_mod, "LOG_DIR", tmp_path / "logs")

    cfg = config_mod.load_default_config()
    cfg["destination_root"] = str(home)
    cfg["targets"] = {"Downloads": True, "Desktop": False, "Documents": False, "Pictures": False}

    monkeypatch.setattr(ui_server_mod, "load_config", lambda path=None: cfg)
    monkeypatch.setattr(organizer_mod, "load_config", lambda path=None: cfg)

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), ClawganizerHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield port, home, downloads
    httpd.shutdown()
    httpd.server_close()


def _get(port: int, path: str):
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request("GET", path)
    res = conn.getresponse()
    body = res.read()
    conn.close()
    return res.status, body


def _post(port: int, path: str, payload: dict):
    data = json.dumps(payload).encode()
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request("POST", path, body=data, headers={"Content-Type": "application/json"})
    res = conn.getresponse()
    body = res.read()
    conn.close()
    return res.status, body


def test_ui_serves_index(ui_server):
    port, _, _ = ui_server
    status, body = _get(port, "/")
    assert status == 200
    assert b"Clawganizer" in body
    assert b"Run" in body
    assert b"tornado.js" in body


def test_ui_status_and_run(ui_server):
    port, home, downloads = ui_server
    status, body = _get(port, "/api/status")
    assert status == 200
    payload = json.loads(body)
    assert payload["pending"] >= 1

    status, body = _post(port, "/api/run", {"apply": True})
    assert status == 200
    result = json.loads(body)
    assert result["move_count"] >= 1
    assert not (downloads / "shot.pdf").exists()
    assert (home / "Documents" / "Organized" / "shot.pdf").exists()
