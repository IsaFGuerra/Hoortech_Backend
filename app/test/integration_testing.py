import os
import tensorflow as tf
import warnings
import absl.logging

# Suprimir logs do TensorFlow e Mediapipe
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Ignora mensagens de info e warning do TensorFlow
warnings.filterwarnings("ignore")  # Ignora todos os warnings Python
absl.logging.set_verbosity(absl.logging.ERROR)  # Limita logs do Mediapipe a apenas erros

from app.handtracking.handtracking import HandTracker
from app.predictor.predictor import LetterPredictor

def carregar_base64_do_arquivo(caminho):
    """Lê a string Base64 de um arquivo de texto."""
    with open(caminho, 'r') as f:
        return f.read()

def test_flow():
    """Testa o fluxo completo de detecção de mão e predição de letra."""
    # Carrega a imagem mock em Base64 do arquivo
    image_mock_base64 = carregar_base64_do_arquivo('app/test/latra-a-base64.txt')

    # Inicializa as classes HandTracker e LetterPredictor
    tracker = HandTracker()
    predictor = LetterPredictor('app/model/model_path.h5')

    # 1. Extrair landmarks da imagem em Base64
    landmarks = tracker.process_frame(image_mock_base64)

    if landmarks:
        print("Landmarks detectados:", landmarks)

        # 2. Usar os landmarks para prever a letra
        predicted_letter = predictor.predict_letter(landmarks)
        print(f"Letra prevista: {predicted_letter}")
    else:
        print("Nenhuma mão detectada.")

# Executa o teste
if __name__ == "__main__":
    test_flow()