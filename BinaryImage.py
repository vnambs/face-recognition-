from flask import Flask, jsonify, request
import cv2
import requests
import numpy as np
from io import BytesIO

app = Flask(__name__)

def recognize_image(image_url):
    # Télécharger l'image à partir de l'URL
    response = requests.get(image_url)
    image = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Convertir l'image en niveaux de gris
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuil sur l'image en niveaux de gris pour la convertir en image binaire
    threshold, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    return binary_image

@app.route("/recognize", methods=["POST"])
def recognize():
    # Récupérer l'URL de l'image à partir des données de la requête
    image_url = request.json["image_url"]

    # Appeler la fonction de reconnaissance d'image avec l'URL de l'image
    binary_image = recognize_image(image_url)

    # Convertir l'image binaire en format base64 pour la retourner dans la réponse JSON
    retval, buffer = cv2.imencode('.jpg', binary_image)
    jpg_as_text = base64.b64encode(buffer)

    # Construire et renvoyer la réponse JSON
    response = {
        "binary_image": jpg_as_text.decode('utf-8')
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run()