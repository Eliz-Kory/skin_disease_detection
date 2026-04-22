"""Train baseline classifier from local train dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier

from ml.inference import SkinConditionModel


def load_rgb(path: Path) -> np.ndarray:
    img = Image.open(path).convert("RGB").resize((224, 224))
    return np.array(img, dtype=np.float32) / 255.0


def collect_dataset(data_dir: Path) -> tuple[np.ndarray, np.ndarray]:
    model = SkinConditionModel()
    x_data: list[np.ndarray] = []
    y_data: list[str] = []

    for class_dir in sorted([p for p in data_dir.iterdir() if p.is_dir()]):
        label = class_dir.name.lower()
        for img_path in class_dir.glob("*"):
            if img_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                continue
            try:
                rgb = load_rgb(img_path)
            except Exception:
                continue
            skin_ratio = model._skin_ratio(rgb)
            features = model._extract_features(rgb, skin_ratio)
            x_data.append(features)
            y_data.append(label)

    if not x_data:
        raise RuntimeError(f"No training images found in {data_dir}")

    return np.array(x_data, dtype=np.float32), np.array(y_data)


def train_and_save(data_dir: Path, out_path: Path) -> None:
    x_train, y_train = collect_dataset(data_dir)
    clf = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        random_state=42,
        class_weight="balanced",
    )
    clf.fit(x_train, y_train)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, out_path)
    print(f"Model saved to: {out_path}")
    print(f"Samples used: {len(y_train)}")
    print(f"Classes: {sorted(set(y_train.tolist()))}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        default="data/train",
        help="Path to train dataset with class subfolders",
    )
    parser.add_argument(
        "--out-model",
        default="models/skin_rf.joblib",
        help="Output model path",
    )
    args = parser.parse_args()
    train_and_save(Path(args.data_dir), Path(args.out_model))


if __name__ == "__main__":
    main()

