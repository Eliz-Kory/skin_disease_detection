from setuptools import setup, find_packages

# Читаем README.md для длинного описания
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Читаем зависимости из requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    # Основная информация
    name="skin_disease_detection",
    version="0.1.0",
    author="Кожакина Анна, Корочкина Елизавета, Муротхонова Гулсанам",
    author_email="kozakina.anna@example.com",  # Можешь указать свою почту
    description="Web-приложение для детекции кожных заболеваний на основе нейронной сети",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eliz-Kory/skin_disease_detection",
    
    # Поиск пакетов
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Требования к Python
    python_requires=">=3.9",
    
    # Зависимости
    install_requires=requirements,
    
    # Дополнительные зависимости (для разработки и документации)
    extras_require={
        "dev": ["pytest", "black", "flake8"],
        "docs": ["sphinx", "sphinx-rtd-theme"],
    },
    
    # Классификаторы (для PyPI)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Development Status :: 3 - Alpha",
    ],
)