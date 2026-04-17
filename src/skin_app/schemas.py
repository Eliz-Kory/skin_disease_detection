"""Schemas and DTOs for API responses."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PredictionResult:
    """Prediction result returned by the classifier service."""

    disease: str
    confidence: float
    severity: str
    severity_score: float
    recommendation: str

    def to_dict(self) -> dict:
        return asdict(self)
