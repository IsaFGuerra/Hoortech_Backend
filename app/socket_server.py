from flask_socketio import SocketIO
from flask import Flask
from flask_cors import CORS
from app.handtracking.handtracking import HandTracker
from app.predictor.predictoralphabet import LetterPredictorAlphabet
# Inicializa o Flask e ativa CORS
app = Flask(__name__)
CORS(app)  # Permitir todas as origens
socketio = SocketIO(app, cors_allowed_origins="*")

# Inicializa HandTracker e LetterPredictor
tracker = HandTracker()
predictor = LetterPredictorAlphabet('app/model/modelo_alphabet.keras')
    
@socketio.on('image_data')
def predict_letter(image_base64):
    """Recebe imagem Base64 e retorna a letra prevista."""
    try:
        if not image_base64:
            return {'status': 400, 'details': 'error: Imagem não recebida.'}

        # Extrair landmarks da imagem
        landmarks = tracker.process_frame(image_base64)

        if landmarks:
            # Prever a letra com base nos landmarks
            predicted_letter = predictor.predict_letter(landmarks)
            print(predict_letter)
            return {'status': 200, 'letter': predicted_letter}
        else:
            return {'status': 400, 'details': 'error: Nenhuma mão detectada.'}

    except Exception as e:
        return {'status': 500, 'details': 'error:' + str(e)}

if __name__ == "__main__":
    # Executa o servidor usando gevent
    socketio.run(app, host='0.0.0.0', port=5003, debug=True)