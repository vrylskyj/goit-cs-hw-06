# Dockerfile

# Використовуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо необхідні бібліотеки
RUN pip install pymongo

# Копіюємо файли до контейнера
COPY . /app
WORKDIR /app

# Запускаємо HTTP сервер та Socket сервер
CMD ["sh", "-c", "python3 main.py & python3 socket_server.py"]
