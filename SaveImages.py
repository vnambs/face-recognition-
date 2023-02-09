import requests
import base64
import cv2
import numpy as np

# Send the request to the Flask application
response = requests.post("http://localhost:5000/recognize", json={"image_url": "https://st2.depositphotos.com/2818715/5612/i/600/depositphotos_56125979-stock-photo-successful-business-team-in-portrait.jpg"})

# Get the binary image from the response
recognized_image = response.json()["recognized_image"]

# Decode the binary image from base64
recognized_image = base64.b64decode(recognized_image)

# Convert the binary image to a numpy array
recognized_image = np.frombuffer(recognized_image, dtype=np.uint8)

# Decode the numpy array to an image
recognized_image = cv2.imdecode(recognized_image, cv2.IMREAD_COLOR)

# Save the image to disk
cv2.imwrite("recognized_image.jpg", recognized_image)
