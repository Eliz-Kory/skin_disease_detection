"""Flask application factory."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, send_from_directory

from .config import AppConfig
from .errors import register_error_handlers
from .model import SkinDiseaseClassifier
from .routes import api_bp
from .services import PredictionService


def create_app(config: AppConfig | None = None) -> Flask:
    """Create and configure Flask app instance."""
    runtime_config = config or AppConfig.from_env()

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = runtime_config.max_content_length
    frontend_dir = Path(__file__).resolve().parents[2] / "frontend"

    classifier = SkinDiseaseClassifier(model_path=runtime_config.model_path)
    app.config["prediction_service"] = PredictionService(
        classifier=classifier,
        allowed_extensions=runtime_config.allowed_extensions,
    )

    @app.get("/")
    def root():
        return send_from_directory(frontend_dir, "index.html")

    @app.get("/assets/<path:filename>")
    def frontend_assets(filename: str):
        return send_from_directory(frontend_dir / "assets", filename)

    @app.get("/api/v1/info")
    def api_info():
        return jsonify(
            {
                "name": runtime_config.app_name,
                "version": runtime_config.version,
                "docs": "Use /api/v1/health and /api/v1/predict endpoints",
            }
        )

    app.register_blueprint(api_bp)
    register_error_handlers(app)
    return app
