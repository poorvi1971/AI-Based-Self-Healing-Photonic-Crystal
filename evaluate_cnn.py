import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from tensorflow.keras.preprocessing.image import ImageDataGenerator


MODEL_PATH = "damage_detector.keras"
IMAGE_SIZE = 100
BATCH_SIZE = 32


# Load trained CNN
model = tf.keras.models.load_model(MODEL_PATH)


# Load dataset
datagen = ImageDataGenerator(
    rescale=1.0 / 255.0
)

test_data = datagen.flow_from_directory(
    "dataset",
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    color_mode="grayscale",
    class_mode="binary",
    batch_size=BATCH_SIZE,
    shuffle=False
)


# Make predictions
probabilities = model.predict(test_data, verbose=0).flatten()

predictions = (probabilities >= 0.5).astype(int)

true_labels = test_data.classes


# Calculate accuracy
accuracy = accuracy_score(true_labels, predictions)


print("\n===================================")
print("CNN MODEL EVALUATION")
print("===================================")

print(f"Accuracy: {accuracy * 100:.2f}%\n")


# Classification report
print("Classification Report:")

print(
    classification_report(
        true_labels,
        predictions,
        target_names=["DAMAGED", "HEALTHY"]
    )
)


# Confusion matrix
cm = confusion_matrix(true_labels, predictions)

print("Confusion Matrix:")
print(cm)


print("\nClass mapping:")
print("0 = DAMAGED")
print("1 = HEALTHY")


print("\n===================================")
print("EVALUATION COMPLETED")
print("===================================")