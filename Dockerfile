# Use a imagem base do Python
FROM python:3.10-slim

# Dependências de sistema (OpenCV / MediaPipe).
# Em Debian 12+ o pacote libgl1-mesa-glx foi removido — use libgl1.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    gcc \
    g++ \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /app

# Adicione o diretório ao PYTHONPATH
ENV PYTHONPATH=/app

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do backend para o contêiner
COPY . .

# Defina a variável de ambiente para produção
ENV FLASK_ENV=production

# Exponha a porta usada pelo Flask
EXPOSE 5003

# Comando para iniciar a aplicação
CMD ["python", "app/socket_server.py"]
