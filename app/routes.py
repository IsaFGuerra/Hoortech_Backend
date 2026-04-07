import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from flask import Blueprint, Response, render_template

main = Blueprint('main', __name__)

# Configuração do modelo Mediapipe para handtracking
base_options = python.BaseOptions(model_asset_path='models/hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

def draw_landmarks_on_image(image, detection_result):
    """Desenha os landmarks detectados na imagem."""
    for hand_landmarks in detection_result.hand_landmarks:
        for landmark in hand_landmarks:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Círculo verde
    return image

def detect_motion():
    """Captura o vídeo e processa a detecção das mãos."""
    cap = cv2.VideoCapture(0)  # Acessa a webcam
    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Converte a imagem para o formato requerido pelo Mediapipe
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Detecta os landmarks
        detection_result = detector.detect(image)

        # Desenha os landmarks na imagem, se houver
        if detection_result.hand_landmarks:
            frame = draw_landmarks_on_image(frame, detection_result)

        # Codifica o frame em JPEG para ser exibido no navegador
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Gera o stream de vídeo
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@main.route('/video_feed')
def video_feed():
    """Endpoint para exibir o feed de vídeo no navegador."""
    return Response(detect_motion(), mimetype='multipart/x-mixed-replace; boundary=frame')

@main.route('/')
def index():
    """Renderiza a página principal."""
    return render_template('index.html')