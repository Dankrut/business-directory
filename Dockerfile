FROM python:3.11.9

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запуск с миграциями
CMD ["sh", "-c", "cd /app && PYTHONPATH=/app alembic upgrade head && python -m src.seed && python src/main.py"]