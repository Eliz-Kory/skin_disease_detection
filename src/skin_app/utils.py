"""Image helpers and recommendation utilities."""

from __future__ import annotations

from io import BytesIO

import numpy as np
from PIL import Image, UnidentifiedImageError

from .errors import ApiError

TARGET_SIZE = (224, 224)


def validate_file_extension(filename: str, allowed_extensions: tuple[str, ...]) -> None:
    """Validate file extension against the accepted list."""
    if "." not in filename:
        raise ApiError("Uploaded file must have an extension", 400)

    ext = filename.rsplit(".", 1)[1].lower()
    if ext not in allowed_extensions:
        raise ApiError(
            f"Unsupported file type '{ext}'. Allowed: {', '.join(allowed_extensions)}",
            400,
        )


def preprocess_image(file_bytes: bytes) -> np.ndarray:
    """Decode and normalize incoming image into model-ready array."""
    try:
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise ApiError("Uploaded file is not a valid image", 400) from exc

    image = image.resize(TARGET_SIZE)
    image_arr = np.array(image, dtype=np.float32) / 255.0
    return image_arr


def get_recommendations(disease: str) -> str:
    """Return basic recommendation text based on prediction class."""
    recommendations = {
        "healthy": "Skin appears healthy. Continue your regular care routine.",
        "eczema": "Use gentle moisturizers and avoid known skin irritants.",
        "psoriasis": "Consult a dermatologist for a tailored treatment plan.",
    }
    return recommendations.get(disease, "Please consult a medical specialist.")