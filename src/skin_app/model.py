"""Model abstraction layer for skin disease classification."""

from __future__ import annotations

import numpy as np

from ml.inference import SkinConditionModel


class SkinDiseaseClassifier:
    """Classifier facade with a placeholder strategy until real model is integrated."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path
        self.model = SkinConditionModel(model_path=model_path)

    def predict(self, image: np.ndarray) -> dict:
        """Predict disease and severity using ML inference pipeline."""
        return self.model.predict(image).to_dict()