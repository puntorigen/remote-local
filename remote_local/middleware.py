# remote_local/middleware.py

import os
import time
import psutil
from pyngrok import ngrok, exception

class NgrokMiddleware:
    def __init__(self, app, port=8000, max_wait_seconds=60, fallback_to_localhost=False, expose_server_info=True):
        self.app = app
        self.port = port
        self.max_wait_seconds = max_wait_seconds
        self.fallback_to_localhost = fallback_to_localhost
        self.expose_server_info = expose_server_info

        app.on_startup(self.startup)

        if expose_server_info:
            self.add_server_info_route()

    async def startup(self):
        public_url = os.getenv("PUBLIC_URL", "").strip()

        if public_url:
            print(f" * [remote-local] Using PUBLIC_URL from environment: {public_url}")
            self.app.state.public_url = public_url
            return

        self.kill_all_ngrok()

        start_time = time.time()
        connected = False

        while not connected and (time.time() - start_time) < self.max_wait_seconds:
            try:
                tunnel = ngrok.connect(self.port)
                public_url = tunnel.public_url
                print(f" * [remote-local] ngrok tunnel created: {public_url}")
                self.app.state.public_url = public_url
                connected = True

            except exception.PyngrokNgrokError as e:
                print(f" * [remote-local] Error connecting ngrok: {e}")
                print(" * [remote-local] Retrying in 5 seconds...")
                time.sleep(5)

        if not connected:
            if self.fallback_to_localhost:
                public_url = f"http://localhost:{self.port}"
                print(f" * [remote-local] Fallback to localhost: {public_url}")
                self.app.state.public_url = public_url
            else:
                raise RuntimeError(f"[remote-local] Could not establish ngrok tunnel after {self.max_wait_seconds} seconds.")

    def kill_all_ngrok(self):
        print(" * [remote-local] Killing existing ngrok processes...")
        for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
            try:
                name = proc.info["name"] or ""
                cmdline = proc.info.get("cmdline") or []
                if "ngrok" in name.lower() or any("ngrok" in cmd.lower() for cmd in cmdline):
                    print(f" * [remote-local] Killing ngrok PID {proc.info['pid']}")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def add_server_info_route(self):
        from fastapi import Request

        @self.app.get("/server-info")
        async def server_info(request: Request):
            public_url = getattr(request.app.state, "public_url", None)
            if public_url is None:
                return {"status": "starting", "public_url": None}
            return {"status": "running", "public_url": public_url}
