import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained model (make sure to use the correct path to your model file)
model = load_model('deepfake_model.h5')  # Replace with your actual model file name

def preprocess_image(image_path):
    # Load image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Resizing as required by the model
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def detect_deepfake(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    return 'Real' if prediction < 0.5 else 'Deepfake'

# Example usage
print(detect_deepfake('path_to_image.jpg'))
