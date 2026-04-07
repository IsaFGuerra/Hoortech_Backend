import numpy as np
import tensorflow as tf

class LetterPredictorVowel:
    def __init__(self, model_path):
        # Carrega o modelo treinado
        self.model = tf.keras.models.load_model(model_path)
        
        self.classes = [
            'A','E','I','O','U',
        ]

    def prepare_data(self, landmarks):
        """Converte os landmarks para um vetor 1D para o modelo."""
        return np.array([value for lm in landmarks for value in [lm['x'], lm['y'], lm['z']]])

    def predict_letter(self, landmarks):
        """Realiza a predição da letra com base nos landmarks."""
        input_data = self.prepare_data(landmarks).reshape(1, -1)
        prediction = self.model.predict(input_data)
        letter_index = np.argmax(prediction)
        predicted_class = self.classes[letter_index]
        return predicted_class  # Retorna a letra prevista