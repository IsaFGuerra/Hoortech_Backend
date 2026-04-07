# Use a imagem base do Python
FROM python:3.10-slim

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libstdc++6 \
    libxrender1 \
    libxext6 \
    gcc \
    g++ \
    build-essential \
    ffmpeg \
    && apt-get clean

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
