"""Application-level exceptions and error handlers."""

from flask import jsonify


class ApiError(Exception):
    """Generic API error with HTTP status code."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def register_error_handlers(app) -> None:
    """Attach error handlers to Flask app."""

    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(413)
    def handle_too_large(_):
        return jsonify({"error": "File is too large"}), 413

    @app.errorhandler(404)
    def handle_not_found(_):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(Exception)
    def handle_unexpected_error(_):
        return jsonify({"error": "Internal server error"}), 500
