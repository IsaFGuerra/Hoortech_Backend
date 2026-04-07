# hoortech_backend

## Arquitetura do Projeto

Este projeto consiste em uma aplicação web que captura a imagem da webcam do usuário, realiza a tradução em tempo real de sinais de Libras e exibe um histórico temporário das traduções que desaparece ao fechar a página. O projeto utiliza Flask como backend, Flask-SocketIO para comunicação em tempo real, OpenCV para captura de vídeo (a ser adicionado futuramente), e PyTorch para o modelo de IA que realizará a tradução (a ser adicionado futuramente).

### V1

```
hoortech_backend/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
├── instance/
│   ├── config.py
├── venv/
├── requirements.txt
└── run.py
```

### V2

```
hoortech_backend/
├── app/
│   ├── __init__.py            # Inicialização da aplicação Flask
│   ├── routes.py              # Definição das rotas Flask
│   ├── models.py              # Modelos de dados e lógica de IA
│   ├── templates/             # Templates HTML para renderização (se necessário)
│   ├── static/                # Arquivos estáticos (CSS, JS, etc.)
│   │   ├── css/
│   │   ├── js/
│   └── services/              # Lógica específica de serviços (como IA e captura de vídeo)
│       ├── __init__.py
│       ├── video_capture.py   # Lógica de captura de vídeo com OpenCV
│       ├── translation.py     # Lógica de tradução de Libras para texto usando IA
│       └── aws_integration.py # Integração com AWS (S3, Rekognition, etc.)
├── instance/
│   ├── config.py              # Configurações específicas do ambiente
├── tests/                     # Testes unitários e de integração
│   ├── __init__.py
│   ├── test_video_capture.py  # Testes para a lógica de captura de vídeo
│   ├── test_translation.py    # Testes para a lógica de tradução de Libras
│   └── test_routes.py         # Testes para as rotas Flask
├── venv/                      # Ambiente virtual
├── requirements.txt           # Lista de dependências do projeto
├── run.py                     # Ponto de entrada para rodar o servidor Flask
└── README.md                  # Documentação do projeto
```

### V3

```
hoortech_backend/
├── app/
│   ├── templates/
│   │   └── index.html           # Interface da aplicação
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css       # Estilos da página web
│   │   └── js/
│   │       └── scripts.js       # Scripts JS para interações em tempo real
│   ├── __init__.py              # Inicialização do Flask e SocketIO
│   ├── routes.py                # Rotas do Flask para lidar com a página principal e traduções
│   └── models.py                # Arquivo para modelagem da IA (futuramente)
├── instance/
│   └── config.py                # Configurações específicas do Flask (futuramente)
├── venv/                        # Ambiente virtual do Python
├── run.py                       # Arquivo principal para iniciar o servidor Flask
└── requirements.txt             # Arquivo de dependências do Python
```

### V4

```
```plaintext
hoortech_backend/
├── app/
│   ├── handtracking/
│   │   └── handtracking.py         # Lógica de detecção de landmarks com MediaPipe
│   ├── model/
│   │   └── model_path.h5           # Modelo TensorFlow para predição de letras
│   ├── predictor/
│   │   └── predictor.py            # Classe responsável pela predição de letras
│   ├── templates/
│   │   └── index.html              # Interface web para interação com o sistema
│   ├── test/
│   │   ├── integration_testing.py  # Teste de integração do fluxo de predição
│   │   ├── letra-a-base64.txt      # Exemplo de imagem codificada em base64
│   │   ├── letra-a.jpg             # Imagem de teste da letra "A"
│   │   ├── routes.py               # Rotas da API Flask
│   │   ├── create_mock_model.py    # Script para gerar um modelo mock de TensorFlow
│   │   └── socket_server.py        # Inicialização do servidor Flask-SocketIO
├── instance/
│   └── config.py                   # Configuração específica de ambiente
├── models/
│   └── hand_landmarker.task        # Arquivo de modelo auxiliar
├── requirements.txt                # Dependências do projeto
├── generate_base64.py              # Script para gerar base64 de uma imagem
├── README.md                       # Documentação do projeto
├── Dockerfile                      # Configuração do Docker para deploy
└── run.py                          # Ponto de entrada do servidor Flask
```

## Passo a Passo para Execução

### Clone o Repositório

```
git clone https://github.com/seu_usuario/hoortech_backend.git
cd hoortech_backend
```

### Crie e Ative o Ambiente Virtual

Windows:
```
python -m venv venv
.\venv\Scripts\activate
```

Linux/MacOS:
```
python3 -m venv venv
source venv/bin/activate
```

### Instale as Dependências

`pip install --no-cache-dir -r requirements.txt`

### Execute o Servidor

`python -m app.socket_server`

### Funcionamento da Aplicação

O Flask subirá um servidor disponível na porta 5003, pronto para receber requisições POST na rota /predict. Ele aguardará uma string Base64 da imagem enviada no corpo da requisição e retornará, em formato JSON, a letra prevista pelo modelo.

### Descrição das Classes

#### 1. HandTracker

Local: app/handtracking/handtracking.py
A classe HandTracker é responsável por processar imagens codificadas em Base64 e extrair landmarks (pontos de referência) da mão. Esses landmarks são posteriormente usados para a predição das letras.

Métodos Principais:

	process_frame(image_base64: str) -> list
Recebe a imagem em Base64, decodifica e utiliza um detector de landmarks para retornar os pontos da mão.
	
	decode_image(image_base64: str) -> np.array
Decodifica a string Base64 para uma imagem utilizável.

####  2. LetterPredictor

Local: app/predictor/predictor.py
A classe LetterPredictor é responsável por carregar o modelo de IA e utilizar landmarks como entrada para prever a letra correspondente.

Métodos Principais:

	__init__(model_path: str)
Inicializa a classe e carrega o modelo salvo no caminho especificado.
	
	predict_letter(landmarks: list) -> str
Recebe uma lista de landmarks e retorna a letra prevista pelo modelo.

####  3. Gerador de Modelo Mock

Local: app/test/create_mock_model.py
Esse script gera um modelo fictício e salva em formato HDF5 para permitir testes de ponta a ponta do sistema.

Função Principal:

	create_mock_model()
Cria e salva um modelo mock que futuramente será substituido pelo modelo treinado.

#### 4. Servidor SocketIO

Local: app/socket_server.py
O servidor é implementado com Flask e Flask-SocketIO, oferecendo uma API para receber imagens codificadas em Base64, processá-las, e retornar a letra prevista.


#### Rota Implementada:

	/predict (Método: POST)
	
Recebe uma imagem em Base64 e retorna a letra prevista com base nos landmarks extraídos.

# Hoortech_Backend
# Hoortech_Backend
# Hoortech_Backend
