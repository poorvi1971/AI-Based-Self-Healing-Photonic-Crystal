import cv2
import numpy as np
import tensorflow as tf

MODEL_PATH = "damage_detector.keras"


def detect_damage(image_path):

    model = tf.keras.models.load_model(MODEL_PATH)

    image = cv2.imread(
        image_path,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    # Resize exactly like training
    image = cv2.resize(
        image,
        (100, 100)
    )

    # Normalize
    image = image.astype("float32") / 255.0

    # Add batch and channel dimensions
    image = np.expand_dims(
        image,
        axis=(0, -1)
    )

    # CNN output = probability of class 1 = HEALTHY
    healthy_probability = float(
        model.predict(
            image,
            verbose=0
        )[0][0]
    )

    damaged_probability = 1.0 - healthy_probability

    if damaged_probability > healthy_probability:

        result = "DAMAGED"
        confidence = damaged_probability
        predicted_class = 0

    else:

        result = "HEALTHY"
        confidence = healthy_probability
        predicted_class = 1

    return {
        "result": result,
        "confidence": confidence,
        "predicted_class": predicted_class,
        "damaged_probability": damaged_probability,
        "healthy_probability": healthy_probability
    }


if __name__ == "__main__":

    print(
        detect_damage(
            "dataset/damaged/damaged_0.png"
        )
    )