import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator


IMAGE_SIZE = 100
BATCH_SIZE = 32
EPOCHS = 30


# ==========================================
# DATASET
# ==========================================

datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    validation_split=0.2,
    rotation_range=5,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=0.05
)


train_data = datagen.flow_from_directory(
    "dataset",
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    color_mode="grayscale",
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training",
    shuffle=True,
    seed=42
)


validation_data = datagen.flow_from_directory(
    "dataset",
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    color_mode="grayscale",
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation",
    shuffle=False,
    seed=42
)


print("\n===================================")
print("CNN DATASET")
print("===================================")

print(
    "Class mapping:",
    train_data.class_indices
)

print(
    "Training images:",
    train_data.samples
)

print(
    "Validation images:",
    validation_data.samples
)


# ==========================================
# CNN MODEL
# ==========================================

model = models.Sequential([

    layers.Input(
        shape=(IMAGE_SIZE, IMAGE_SIZE, 1)
    ),

    layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(
        (2, 2)
    ),

    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(
        (2, 2)
    ),

    layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(
        (2, 2)
    ),

    layers.Flatten(),

    layers.Dense(
        128,
        activation="relu"
    ),

    layers.Dropout(
        0.4
    ),

    layers.Dense(
        1,
        activation="sigmoid"
    )
])


# ==========================================
# COMPILE
# ==========================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0003
    ),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


# ==========================================
# CALLBACKS
# ==========================================

callbacks = [

    tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        patience=6,
        restore_best_weights=True
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        min_lr=0.00001
    )
]


# ==========================================
# TRAIN
# ==========================================

print("\n===================================")
print("STARTING CNN TRAINING")
print("===================================\n")


history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=EPOCHS,
    callbacks=callbacks
)


# ==========================================
# BEST RESULTS
# ==========================================

best_train_accuracy = max(
    history.history["accuracy"]
)

best_validation_accuracy = max(
    history.history["val_accuracy"]
)


print("\n===================================")
print("CNN TRAINING COMPLETED")
print("===================================")

print(
    f"Best Training Accuracy: "
    f"{best_train_accuracy * 100:.2f}%"
)

print(
    f"Best Validation Accuracy: "
    f"{best_validation_accuracy * 100:.2f}%"
)


# ==========================================
# SAVE MODEL
# ==========================================

model.save(
    "damage_detector.keras"
)

print("\nModel saved as:")
print("damage_detector.keras")

print("===================================")