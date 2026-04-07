import os
import threading

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Carregamento preguiçoso: Render exige que a porta abra rápido; TF + modelo demoram demais no import.
_tracker = None
_predictor = None
_load_lock = threading.Lock()


def get_tracker():
    global _tracker
    with _load_lock:
        if _tracker is None:
            from app.handtracking.handtracking import HandTracker

            _tracker = HandTracker()
        return _tracker


def get_predictor():
    global _predictor
    with _load_lock:
        if _predictor is None:
            from app.predictor.predictoralphabet import LetterPredictorAlphabet

            _predictor = LetterPredictorAlphabet("app/model/modelo_alphabet.keras")
        return _predictor


@app.route("/")
def health():
    """Health check para o provedor (Render) e verificação rápida."""
    return {"status": "ok"}, 200


@socketio.on("image_data")
def predict_letter(image_base64):
    """Recebe imagem Base64 e retorna a letra prevista."""
    try:
        if not image_base64:
            return {"status": 400, "details": "error: Imagem não recebida."}

        tracker = get_tracker()
        landmarks = tracker.process_frame(image_base64)

        if landmarks:
            predictor = get_predictor()
            predicted_letter = predictor.predict_letter(landmarks)
            print(predicted_letter)
            return {"status": 200, "letter": predicted_letter}
        return {"status": 400, "details": "error: Nenhuma mão detectada."}

    except Exception as e:
        return {"status": 500, "details": "error:" + str(e)}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5003"))
    debug = os.environ.get("FLASK_ENV") != "production"
    socketio.run(app, host="0.0.0.0", port=port, debug=debug)
