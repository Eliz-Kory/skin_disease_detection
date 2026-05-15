"""Business services for prediction flow."""

from __future__ import annotations

from .errors import ApiError
from .model import SkinDiseaseClassifier
from .schemas import PredictionResult
from .utils import get_recommendations, preprocess_image, validate_file_extension


class PredictionService:
    """Coordinates image validation, preprocessing, inference and response mapping."""

    def __init__(
        self, classifier: SkinDiseaseClassifier, allowed_extensions: tuple[str, ...]
    ) -> None:
        self.classifier = classifier
        self.allowed_extensions = allowed_extensions

    def predict_from_upload(self, file_storage) -> PredictionResult:
        if not file_storage:
            raise ApiError("No file provided", 400)

        filename = (file_storage.filename or "").strip()
        if not filename:
            raise ApiError("Filename is empty", 400)

        validate_file_extension(filename, self.allowed_extensions)
        file_bytes = file_storage.read()
        if not file_bytes:
            raise ApiError("Uploaded file is empty", 400)

        image = preprocess_image(file_bytes)
        prediction = self.classifier.predict(image)
        if not prediction.get("detectable", True):
            raise ApiError(prediction.get("recommendation", "Не удалось распознать кожу на изображении."), 422)
        disease = prediction["disease"]
        return PredictionResult(
            disease=disease,
            confidence=float(prediction["confidence"]),
            severity=prediction.get("severity", "не определена"),
            severity_score=float(prediction.get("severity_score", 0.0)),
            recommendation=prediction.get("recommendation", get_recommendations(disease)),
        )
