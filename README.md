# remote-local

Expose your local FastAPI, NiceGUI, or development servers remotely — easily, reliably, and for free.

**remote-local** is a simple and robust middleware that automatically creates a public tunnel for your local server using ngrok (and more in the future).  
It handles session cleanup, hot reloads, and retries automatically — no manual setup required.

---

## Features

- 🌍 Expose your local server remotely with **one line of code**.
- ⚡ Fully compatible with **FastAPI**, **NiceGUI**, or any **ASGI app**.
- 🔄 **Handles hot reloads** and session recovery automatically.
- 🔒 **No external configuration** required — works with free ngrok accounts.
- 🛠️ Designed for **development, testing, and remote integrations**.

---

## Installation

```bash
pip install remote-local
```

---

## Quick Usage

```python
from nicegui import app, ui
from remote_local import NgrokMiddleware

NgrokMiddleware(app, port=8080)

@ui.page('/')
async def main_page():
    ui.label('Hello World')

ui.run(port=8080, reload=True)
```

✅ That's it! Your local server is now publicly accessible through a secure URL.

By default, a `/server-info` endpoint is also created, showing the current public URL and server status.

---

## Configuration Options

You can customize the middleware:

```python
NgrokMiddleware(
    app,
    port=8080,
    max_wait_seconds=60,    # how long to retry if ngrok fails initially
    fallback_to_localhost=False,  # fallback to localhost if ngrok fails
    expose_server_info=True,      # create a /server-info endpoint
)
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Future Plans

- Support for other tunnels (Cloudflared, Localhost.run, etc.)
- More flexible server info APIs
- Auto-detection of multiple servers

---

## Author

Made with ❤️ by Pablo Schaffner
