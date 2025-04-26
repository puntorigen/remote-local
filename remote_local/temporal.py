# remote_local/temporal.py

from contextlib import contextmanager
from pyngrok import ngrok
import psutil

# Estado compartido
_current_tunnel = None
_tunnel_refcount = 0

def kill_all_ngrok():
    print(" * [remote-local] Killing existing ngrok processes (temporal_url)...")
    for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        try:
            name = proc.info["name"] or ""
            cmdline = proc.info.get("cmdline") or []
            if "ngrok" in name.lower() or any("ngrok" in cmd.lower() for cmd in cmdline):
                print(f" * [remote-local] Killing ngrok PID {proc.info['pid']}")
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

@contextmanager
def temporal_url(port=8000):
    """
    Context manager to create or reuse a temporary public URL for your local server.

    Args:
        port (int): Local port to expose. Default is 8000.

    Yields:
        public_url (str): The public URL created or reused.
    """
    global _current_tunnel, _tunnel_refcount

    if _current_tunnel is None:
        kill_all_ngrok()
        _current_tunnel = ngrok.connect(port)
        print(f" * [remote-local] Temporal URL created: {_current_tunnel.public_url}")
    
    _tunnel_refcount += 1
    try:
        yield _current_tunnel.public_url
    finally:
        _tunnel_refcount -= 1
        if _tunnel_refcount == 0:
            print(f" * [remote-local] Closing temporal URL: {_current_tunnel.public_url}")
            ngrok.disconnect(_current_tunnel.public_url)
            kill_all_ngrok()
            _current_tunnel = None
