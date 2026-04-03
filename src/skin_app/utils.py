"""
Вспомогательные функции для обработки изображений.
"""

import numpy as np
from PIL import Image


def preprocess_image(image_path):
    """
    Предобработка изображения перед подачей в модель.
    
    Args:
        image_path: Путь к изображению или файловый объект.
        
    Returns:
        numpy.ndarray: Обработанное изображение.
    """
    img = Image.open(image_path)
    img = img.resize((224, 224))
    return np.array(img)


def get_recommendations(disease):
    """
    Получение рекомендаций по лечению заболевания.
    
    Args:
        disease: Название заболевания.
        
    Returns:
        str: Рекомендации по лечению.
    """
    recommendations = {
        'healthy': 'Ваша кожа здорова! Продолжайте ухаживать за ней.',
        'eczema': 'Рекомендуется использовать увлажняющие кремы.',
        'psoriasis': 'Обратитесь к дерматологу для назначения лечения.'
    }
    return recommendations.get(disease, 'Обратитесь к врачу.')