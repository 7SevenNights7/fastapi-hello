FROM python:3.12-slim

# Устанавливаем зависимости для Python и системы
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Сначала зависимости (чтобы кэшировалось)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом код
COPY main.py .

# Запускаем uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
