# Развертывание приложения в Docker

## Назначение
Файл `Dockerfile` упаковывает backend Flask API, frontend-страницу и ML-модуль в единый контейнер. Настройки, которые могут меняться между локальной и серверной средой, передаются через переменные окружения.

## Переменные окружения

| Переменная | Назначение | Значение по умолчанию |
|---|---|---|
| `MODEL_PATH` | Путь к файлу обученной модели внутри контейнера | `/app/models/skin_rf.joblib` |
| `FLASK_DEBUG` | Режим отладки Flask | `0` |

## Сборка и запуск Docker

```bash
docker build -t skin-disease-detection .
docker run --rm -p 5000:5000 -e MODEL_PATH=/app/models/skin_rf.joblib -v "%cd%/models:/app/models:ro" skin-disease-detection
```

Для Linux/MacOS:

```bash
docker run --rm -p 5000:5000 -e MODEL_PATH=/app/models/skin_rf.joblib -v "$(pwd)/models:/app/models:ro" skin-disease-detection
```

## Запуск через docker-compose

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:5000
```

Проверка backend API:

```text
http://127.0.0.1:5000/api/v1/health
```

## Что входит в контейнер
- `app.py` - точка входа приложения;
- `src/skin_app` - backend Flask API;
- `frontend` - статическая клиентская часть;
- `ml` - модуль инференса модели;
- `requirements.txt` и `setup.py` - зависимости и установка проекта.

## Примечание по модели
Файл модели не включается в Docker-образ через `.dockerignore`, потому что веса могут быть крупными. Поэтому папка `models/` подключается как внешний volume. Это соответствует требованию получать внешние ресурсы через параметры окружения и не зашивать их жестко в образ.
