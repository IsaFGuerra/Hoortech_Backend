import base64
import cv2
import numpy as np
import mediapipe as mp

class HandTracker:
    def __init__(self):
        # Inicializa o Mediapipe para detectar mãos
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=1)

    def decode_image(self, image_base64):
        """Decodifica a imagem em Base64 para o formato OpenCV."""
        # Remove prefixo se presente
        image_base64 = image_base64.split(',')[1] if ',' in image_base64 else image_base64

        # Ajusta o padding da string Base64, se necessário
        missing_padding = len(image_base64) % 4
        if missing_padding != 0:
            image_base64 += '=' * (4 - missing_padding)

        # Decodifica a imagem
        image_data = base64.b64decode(image_base64)
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img

    def process_frame(self, image_base64):
        """Processa a imagem e retorna os landmarks detectados."""
        img = self.decode_image(image_base64)
        if img is None:
            raise ValueError("Falha ao decodificar a imagem.")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                return [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in hand_landmarks.landmark]
        return None