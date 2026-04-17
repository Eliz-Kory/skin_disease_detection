"""HTTP routes for API v1."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from .services import PredictionService

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.get("/health")
def healthcheck():
    """Basic health endpoint for runtime checks."""
    return jsonify({"status": "ok", "service": "skin-disease-backend"})


@api_bp.post("/predict")
def predict():
    """Predict skin condition from uploaded image."""
    file = request.files.get("file")
    service: PredictionService = current_app.config["prediction_service"]
    result = service.predict_from_upload(file)
    return jsonify(result.to_dict()), 200
