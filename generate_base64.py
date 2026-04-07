import base64

# Caminho para a imagem
image_path = 'app/test/letra-a.jpg'

# Ler e codificar a imagem em Base64
with open(image_path, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

print(f"data:image/jpeg;base64,{encoded_string}")