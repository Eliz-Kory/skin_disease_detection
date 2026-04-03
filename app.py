# app.py

from flask import Flask, request, render_template
from src.skin_app.model import SkinDiseaseClassifier  # Импорт твоей нейросети
from src.skin_app.utils import process_image          # Импорт обработки фото

# 1. Создание приложения
app = Flask(__name__)

# Загрузка модели при старте (чтобы не грузить каждый раз заново)
model = SkinDiseaseClassifier("models/best_model.pth")

@app.route('/')
def index():
    """
    Главная страница сайта.
    
    Returns:
        str: HTML-шаблон главной страницы.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Обработка загруженного изображения и выдача прогноза.
    
    Returns:
        str: HTML-шаблон с результатом анализа.
    """
    if 'file' not in request.files:
        return "Нет файла", 400
    
    file = request.files['file']
    # Логика: сохранить -> обработать -> предсказать
    image = process_image(file)
    result = model.predict(image)
    
    return render_template('result.html', disease=result['disease'])

if __name__ == '__main__':
    """
    Запуск сервера в режиме отладки.
    """
    app.run(debug=True)
    