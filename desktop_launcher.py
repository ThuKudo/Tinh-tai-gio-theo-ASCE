from __future__ import annotations

import socket
import sys
import threading
import time
import traceback
import webbrowser
from pathlib import Path

import uvicorn

from app.main import app


def find_available_port(start_port: int = 8000, end_port: int = 8010) -> int:
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise RuntimeError("No available local port found in the range 8000-8010.")


def open_browser(port: int) -> None:
    time.sleep(1.5)
    webbrowser.open(f"http://127.0.0.1:{port}")


def log_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().with_name("WinLoadASCEApp-error.log")
    return Path(__file__).resolve().with_name("WinLoadASCEApp-error.log")


if __name__ == "__main__":
    try:
        port = find_available_port()
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()
        config = uvicorn.Config(
            app=app,
            host="127.0.0.1",
            port=port,
            reload=False,
            log_config=None,
            access_log=False,
        )
        server = uvicorn.Server(config)
        server.run()
    except Exception:
        log_path().write_text(traceback.format_exc(), encoding="utf-8")
        raise
