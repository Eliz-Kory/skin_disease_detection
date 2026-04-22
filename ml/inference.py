"""Skin image analysis and disease classification helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

try:
    import joblib
except ImportError:  # pragma: no cover - fallback for minimal runtime environments
    joblib = None


@dataclass(frozen=True)
class InferenceResult:
    """Normalized output contract for backend API."""

    detectable: bool
    disease: str | None
    confidence: float
    severity: str | None
    severity_score: float
    recommendation: str

    def to_dict(self) -> dict:
        return {
            "detectable": self.detectable,
            "disease": self.disease,
            "confidence": self.confidence,
            "severity": self.severity,
            "severity_score": self.severity_score,
            "recommendation": self.recommendation,
        }


class SkinConditionModel:
    """Feature-based baseline model with optional trained sklearn classifier."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path
        self.classes = ["healthy", "eczema", "psoriasis"]
        self.clf = self._load_classifier(model_path)

    def _load_classifier(self, model_path: str | None):
        if not model_path:
            return None
        if joblib is None:
            return None
        path = Path(model_path)
        if not path.exists():
            return None
        try:
            return joblib.load(path)
        except Exception:
            return None

    def predict(self, rgb_image: np.ndarray) -> InferenceResult:
        skin_ratio = self._skin_ratio(rgb_image)
        if skin_ratio < 0.18:
            return InferenceResult(
                detectable=False,
                disease=None,
                confidence=0.0,
                severity=None,
                severity_score=0.0,
                recommendation="Изображение не похоже на кожу. Загрузите четкое фото участка кожи крупным планом.",
            )

        features = self._extract_features(rgb_image, skin_ratio)
        disease, confidence = self._classify(features)
        severity_score, severity = self._estimate_severity(features)
        recommendation = self._recommendation(disease, severity, severity_score)

        return InferenceResult(
            detectable=True,
            disease=disease,
            confidence=confidence,
            severity=severity,
            severity_score=severity_score,
            recommendation=recommendation,
        )

    def _extract_features(self, rgb_image: np.ndarray, skin_ratio: float) -> np.ndarray:
        img_u8 = (np.clip(rgb_image, 0.0, 1.0) * 255).astype(np.uint8)
        hsv = cv2.cvtColor(img_u8, cv2.COLOR_RGB2HSV)

        h = hsv[:, :, 0]
        s = hsv[:, :, 1].astype(np.float32) / 255.0
        v = hsv[:, :, 2].astype(np.float32) / 255.0

        redness_mask = ((h < 12) | (h > 170)) & (s > 0.25) & (v > 0.2)
        redness_ratio = float(redness_mask.mean())
        mean_redness = float(s[redness_mask].mean()) if redness_mask.any() else 0.0

        gray = cv2.cvtColor(img_u8, cv2.COLOR_RGB2GRAY)
        lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var() / 1000.0)

        lesion_area = float(np.clip(redness_ratio * 2.5, 0.0, 1.0))

        return np.array(
            [
                skin_ratio,
                redness_ratio,
                mean_redness,
                float(s.mean()),
                float(v.mean()),
                lap_var,
                lesion_area,
            ],
            dtype=np.float32,
        )

    def _skin_ratio(self, rgb_image: np.ndarray) -> float:
        img_u8 = (np.clip(rgb_image, 0.0, 1.0) * 255).astype(np.uint8)
        hsv = cv2.cvtColor(img_u8, cv2.COLOR_RGB2HSV)
        ycrcb = cv2.cvtColor(img_u8, cv2.COLOR_RGB2YCrCb)

        lower_hsv = np.array([0, 18, 40], dtype=np.uint8)
        upper_hsv = np.array([30, 170, 255], dtype=np.uint8)
        mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

        lower_ycrcb = np.array([0, 133, 77], dtype=np.uint8)
        upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)
        mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

        skin_mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)
        return float((skin_mask > 0).mean())

    def _classify(self, features: np.ndarray) -> tuple[str, float]:
        if self.clf is not None:
            probs = self.clf.predict_proba([features])[0]
            idx = int(np.argmax(probs))
            return self.clf.classes_[idx], float(probs[idx])

        _, redness_ratio, mean_redness, sat_mean, _, texture, _ = features.tolist()
        if redness_ratio < 0.05 and mean_redness < 0.32:
            return "healthy", 0.78
        if texture > 0.18 and sat_mean > 0.35:
            return "psoriasis", 0.74
        return "eczema", 0.72

    def _estimate_severity(self, features: np.ndarray) -> tuple[float, str]:
        _, redness_ratio, mean_redness, _, _, _, lesion_area = features.tolist()
        score = float(np.clip(0.55 * lesion_area + 0.45 * (redness_ratio + mean_redness) / 2, 0.0, 1.0))
        if score < 0.33:
            return score, "легкая"
        if score < 0.66:
            return score, "средняя"
        return score, "тяжелая"

    def _recommendation(self, disease: str, severity: str, severity_score: float) -> str:
        severity_note = f"Степень выраженности: {severity} ({int(severity_score * 100)}%)."
        if disease == "healthy":
            return f"Признаки воспаления минимальны. Продолжайте базовый уход и защиту кожи от пересушивания. {severity_note}"
        if disease == "eczema":
            return (
                "Похоже на экзему: используйте эмоленты 2-3 раза в день, избегайте агрессивных моющих средств "
                "и аллергенов. При усилении симптомов обратитесь к дерматологу. "
                f"{severity_note}"
            )
        return (
            "Похоже на псориаз: рекомендуется консультация дерматолога, регулярное увлажнение и наблюдение за "
            "динамикой очагов. Не занимайтесь самолечением гормональными препаратами без врача. "
            f"{severity_note}"
        )
        if disease == "acne":
            return (
                "Похоже на акне: используйте мягкое очищение 2 раза в день, не травмируйте воспаления, "
                "избегайте комедогенной косметики. При выраженном воспалении обратитесь к дерматологу. "
                f"{severity_note}"
            )
        if disease in {"eksim", "ekzema"}:
            return (
                "Похоже на экзему: применяйте эмоленты, избегайте раздражителей и длительного контакта с водой. "
                "При зуде и ухудшении нужна очная консультация специалиста. "
                f"{severity_note}"
            )
        if disease == "herpes":
            return (
                "Похоже на герпетическое поражение: не травмируйте очаг, соблюдайте гигиену, "
                "по возможности обратитесь к врачу для противовирусной терапии. "
                f"{severity_note}"
            )
        if disease == "rosacea":
            return (
                "Похоже на розацеа: избегайте провоцирующих факторов (перегрев, алкоголь, острое), "
                "используйте щадящий уход и солнцезащиту. Нужна консультация дерматолога для схемы лечения. "
                f"{severity_note}"
            )
        if disease == "panu":
            return (
                "Возможны признаки грибкового поражения кожи. Поддерживайте сухость пораженной зоны и "
                "обратитесь к дерматологу для подбора противогрибковой терапии. "
                f"{severity_note}"
            )
        return (
            "Обнаружены признаки кожного состояния. Рекомендуется очная консультация дерматолога "
            "для подтверждения диагноза и подбора лечения. "
            f"{severity_note}"
        )

