"""
Gera um modelo Keras compatível com LetterPredictorAlphabet para testes locais/deploy
sem dataset real. As predições serão aleatórias (pesos não treinados de verdade).

Classes: 21 letras em predictoralphabet.py | Entrada: 63 (21 landmarks × xyz).
"""
import os

import numpy as np
import tensorflow as tf

# Deve coincidir com len(LetterPredictorAlphabet.classes)
NUM_CLASSES = 21
INPUT_DIM = 63  # MediaPipe hand: 21 landmarks × (x, y, z)

OUT_DIR = os.path.join(os.path.dirname(__file__), "model")
OUT_PATH = os.path.join(OUT_DIR, "modelo_alphabet.keras")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(128, activation="relu", input_shape=(INPUT_DIM,)),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(NUM_CLASSES, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    dummy_x = np.random.random((8, INPUT_DIM)).astype(np.float32)
    dummy_y = np.random.randint(0, NUM_CLASSES, size=(8,))
    model.fit(dummy_x, dummy_y, epochs=1, verbose=0)

    model.save(OUT_PATH)
    print(f"Modelo mock salvo em: {OUT_PATH}")


if __name__ == "__main__":
    main()
