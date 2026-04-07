import tensorflow as tf
import numpy as np

# Definir um modelo mock simples para teste
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(63,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(26, activation='softmax')  # 26 letras do alfabeto
])

# Compilar o modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Treinar o modelo com dados mock
dummy_input = np.random.random((1, 63))  # Mock: 63 features
dummy_output = np.array([0])  # Mock: Saída correspondente à letra 'A'

model.fit(dummy_input, dummy_output, epochs=1, verbose=0)

# Salvar o modelo no formato .h5
model.save('app/model/model_path.h5')

print("Modelo mock salvo com sucesso!")