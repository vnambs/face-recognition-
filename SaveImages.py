import requests
import base64 as b64
import os


# URL de l'API Flask
url = "http://localhost:5000/recognize"

# Données de la requête POST, incluant l'URL de l'image
data = { "image_url": "https://st2.depositphotos.com/2818715/5612/i/600/depositphotos_56125979-stock-photo-successful-business-team-in-portrait.jpg" }

# Envoyer la requête POST à l'API
response = requests.post(url, json=data)

# Vérifier que la réponse est correcte
if response.status_code == 200:
    # Décoder la réponse JSON
    response_data = response.json()

    # Récupérer l'image complète avec les visages détectés
    image_data = response_data["image"]
    image_data = image_data.encode("utf-8")

    # Enregistrer l'image sur le disque
    image_bytes = b64.decodebytes(image_data)
    with open("image_with_faces.jpg", "wb") as f:
        f.write(image_bytes)

    # Récupérer les images des visages détectés
    face_images = response_data["faces"]

    # Enregistrer chaque image de visage sur le disque
    for i, face_image in enumerate(face_images):
        face_image = face_image.encode("utf-8")
        with open(f"face_{i}.jpg", "wb") as f:
            f.write(b64.b64decode(face_image))

else:
    # Afficher un message d'erreur si la réponse n'est pas correcte
    print("Error:", response.text)
