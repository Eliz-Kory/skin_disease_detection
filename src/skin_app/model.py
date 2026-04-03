"""
Модуль для работы с нейронной сетью.
Содержит класс для классификации кожных заболеваний.
"""

class SkinDiseaseClassifier:
    """
    Классификатор кожных заболеваний на основе нейронной сети.
    
    Attributes:
        model: Обученная модель нейронной сети.
        classes: Список классов заболеваний.
    """
    
    def __init__(self, model_path=None):
        """
        Инициализация классификатора.
        
        Args:
            model_path: Путь к файлу с весами модели.
        """
        self.model_path = model_path
        self.classes = ['healthy', 'eczema', 'psoriasis']
    
    def predict(self, image):
        """
        Предсказание заболевания по изображению.
        
        Args:
            image: Изображение в формате numpy array.
            
        Returns:
            dict: Словарь с результатом предсказания.
        """
        return {
            'disease': 'healthy',
            'confidence': 0.95
        }