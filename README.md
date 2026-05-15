# Skin Disease Detection

Веб-приложение для детекции кожных заболеваний по фотографии.

## Описание
Пользователь загружает фото участка кожи → нейросеть определяет заболевание → выдаются рекомендации по лечению.

## Стек
- Python 3.10+, Flask
- PyTorch, OpenCV, Pillow
- setuptools, Sphinx

## Запуск
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python app.py