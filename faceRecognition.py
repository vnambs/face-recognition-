from flask import Flask, jsonify, request
import cv2
import base64 as b64
import requests
import numpy as np
from io import BytesIO

app = Flask(__name__)

def recognize_face(image_url):
    # Télécharger l'image à partir de l'URL
    response = requests.get(image_url)
    image = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Charger les classificateurs de visage pré-entraînés
    face_cascade1 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_cascade2 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    face_cascade3 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    face_cascade4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

  
    # Convertir l'image en niveaux de gris pour une détection plus rapide
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

     # Détecter les visages dans l'image en niveaux de gris en utilisant les deux classificateurs
    faces1 = face_cascade1.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    faces2 = face_cascade2.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)    
    faces3 = face_cascade3.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)    
    faces4 = face_cascade4.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

    # Fusionner les résultats des deux classificateurs
    faces = np.concatenate((faces1, faces2, faces3, faces4))

    face_images = []
    # Dessiner un rectangle autour des visages détectés
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

         # Extraire le visage de l'image
        face_image = image[y:y+h, x:x+w]

        # Convertir l'image en format base64 pour la retourner dans la réponse JSON
        retval, buffer = cv2.imencode('.jpg', face_image)
        jpg_as_text = b64.b64encode(buffer).decode('utf-8')
        face_images.append(jpg_as_text)

    return image, face_images

@app.route("/recognize", methods=["POST"])
def recognize():
    # Récupérer l'URL de l'image à partir des données de la requête
    image_url = request.json["image_url"]

    # Appeler la fonction de reconnaissance d'image avec l'URL de l'image
    image, face_images = recognize_face(image_url)

    # Convertir l'image avec les visages détectés en format base64 pour la retourner dans la réponse JSON
    retval, buffers = cv2.imencode('.jpg', image)
    image_with_faces = b64.b64encode(buffers).decode('utf-8')


   # Construire et renvoyer la réponse JSON
    response = {
        "image": image_with_faces,
        "faces": face_images,
        "face_count":len(face_images)
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)