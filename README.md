# face-recognition API - Python & Flask

## Prérequis

  * Python 3.x
  * OpenCV
  * Flask
  * Requests
  * Nump

## Installation
1. Clonez ce dépôt sur votre machine local :
  
  ```bash 
  git clone https://github.com/yourusername/face-recognition-flask.git
2. Installez les dépendances nécessaires en utilisant pip :

  ```bash
  pip install opencv-python flask requests numpy

3. Démarrez le serveur Flask :

  ```bash
  python face-recognition-flask.py

## Utilisation
Envoyez une requête POST à l'URL /recognize en incluant l'URL de l'image à reconnaître dans le corps de la requête :
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"image_url": "https://example.com/image.jpg"}' http://localhost:5000/recognize

Vous recevrez une réponse JSON contenant l'image reconnue en format base64.

###Remarques
Assurez-vous que le classificateur de visage Haar (fichier XML) se trouve dans le même répertoire que le fichier Python.
Vous pouvez ajouter d'autres classificateurs pour améliorer la reconnaissance de visage en les chargeant dans la fonction recognize_face.
