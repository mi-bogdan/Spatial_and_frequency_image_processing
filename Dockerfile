# Используем образ Python
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1 

WORKDIR /code 

COPY requirements.txt /code/

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libqt5x11extras5 \
    qt5dxcb-plugin \
    xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

RUN pip install -r requirements.txt 

COPY . /code/

CMD ["python", "main.py"]