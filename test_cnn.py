import tensorflow as tf
import numpy as np
from PIL import Image

# Load trained CNN
model = tf.keras.models.load_model("damage_detector.keras")

# Test image
image_path = "dataset/damaged/damaged_0.png"

# Load and prepare image
image = Image.open(image_path).convert("L")
image = image.resize((100, 100))

image_array = np.array(image, dtype=np.float32)
image_array = image_array / 255.0

# Add batch and channel dimensions
image_array = image_array.reshape(1, 100, 100, 1)

# CNN prediction
prediction = model.predict(image_array, verbose=0)

class_names = ["damaged", "healthy"]

predicted_class = np.argmax(prediction[0])
confidence = prediction[0][predicted_class] * 100

print("Prediction:", class_names[predicted_class])
print("Confidence:", round(confidence, 2), "%")