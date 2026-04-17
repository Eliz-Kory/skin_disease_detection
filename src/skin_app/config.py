"""Application configuration."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for the API server."""

    app_name: str = "Skin Disease Detection API"
    version: str = "0.1.0"
    max_content_length: int = 5 * 1024 * 1024
    allowed_extensions: tuple[str, ...] = ("jpg", "jpeg", "png", "webp")
    model_path: str = "models/skin_rf.joblib"
    debug: bool = False

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Build configuration from environment variables."""
        return cls(
            model_path=os.getenv("MODEL_PATH", cls.model_path),
            debug=os.getenv("FLASK_DEBUG", "0") == "1",
        )
