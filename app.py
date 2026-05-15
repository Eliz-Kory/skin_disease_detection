"""Application entry point for local and container deployment."""

from src.skin_app.app_factory import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))
