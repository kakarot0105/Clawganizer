"""Local HTTP server for the Clawganizer UI."""

from __future__ import annotations

import json
import mimetypes
import threading
import webbrowser
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .. import __version__
from ..config import USER_CONFIG_PATH, load_config
from ..organizer import (
    OrganizeResult,
    enabled_source_dirs,
    organize,
    plan_moves,
    summarize_by_category,
    undo_last_run,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


def _result_payload(result: OrganizeResult) -> dict[str, Any]:
    return {
        "moved": [asdict(m) for m in result.moved],
        "skipped": result.skipped,
        "errors": result.errors,
        "log_path": result.log_path,
        "move_count": result.move_count,
        "by_category": summarize_by_category(result.moved),
    }


def _status_payload() -> dict[str, Any]:
    config = load_config()
    planned = plan_moves(config)
    sources = enabled_source_dirs(config)
    return {
        "version": __version__,
        "home": str(Path.home()),
        "pending": len(planned),
        "by_category": summarize_by_category(planned),
        "targets": [
            {
                "name": name,
                "enabled": bool(enabled),
                "exists": (Path.home() / name).is_dir(),
                "path": str(Path.home() / name),
            }
            for name, enabled in config.get("targets", {}).items()
        ],
        "sources": [str(p) for p in sources],
        "config_path": str(USER_CONFIG_PATH) if USER_CONFIG_PATH.exists() else None,
        "preview": [
            {
                "source": m.source,
                "destination": m.destination,
                "category": m.category,
            }
            for m in planned[:60]
        ],
    }


class ClawganizerHandler(BaseHTTPRequestHandler):
    server_version = f"ClawganizerUI/{__version__}"

    def log_message(self, fmt: str, *args: Any) -> None:
        # Keep terminal quiet unless useful.
        if self.path.startswith("/api/"):
            super().log_message(fmt, *args)

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, code: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload).encode("utf-8")
        self._send(code, data, "application/json; charset=utf-8")

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/status":
            self._send_json(200, _status_payload())
            return
        if path == "/api/health":
            self._send_json(200, {"ok": True, "version": __version__})
            return

        rel = "index.html" if path in ("", "/") else path.lstrip("/")
        # Prevent path traversal
        candidate = (STATIC_DIR / rel).resolve()
        if not str(candidate).startswith(str(STATIC_DIR.resolve())):
            self._send_json(403, {"error": "forbidden"})
            return
        if not candidate.is_file():
            self._send_json(404, {"error": "not found"})
            return
        data = candidate.read_bytes()
        ctype, _ = mimetypes.guess_type(str(candidate))
        self._send(200, data, ctype or "application/octet-stream")

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            body = self._read_json()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid JSON"})
            return

        if path == "/api/run":
            apply_moves = bool(body.get("apply", True))
            try:
                result = organize(dry_run=not apply_moves)
            except Exception as exc:  # noqa: BLE001 — surface to UI
                self._send_json(500, {"error": str(exc)})
                return
            payload = _result_payload(result)
            payload["applied"] = apply_moves
            self._send_json(200, payload)
            return

        if path == "/api/undo":
            dry_run = bool(body.get("dry_run", False))
            try:
                result = undo_last_run(dry_run=dry_run)
            except Exception as exc:  # noqa: BLE001
                self._send_json(500, {"error": str(exc)})
                return
            self._send_json(200, _result_payload(result))
            return

        self._send_json(404, {"error": "not found"})


def serve_ui(
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    open_browser: bool = True,
) -> None:
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), ClawganizerHandler)
    url = f"http://{host}:{port}/"
    print(f"Clawganizer UI {__version__}")
    print(f"Open: {url}")
    print("Press Ctrl+C to stop.")

    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()
