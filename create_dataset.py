import os
import cv2
import numpy as np

IMAGE_SIZE = 200
NUM_IMAGES = 2000

HEALTHY_DIR = "dataset/healthy"
DAMAGED_DIR = "dataset/damaged"

os.makedirs(HEALTHY_DIR, exist_ok=True)
os.makedirs(DAMAGED_DIR, exist_ok=True)


def create_photonic_crystal():

    image = np.ones(
        (IMAGE_SIZE, IMAGE_SIZE),
        dtype=np.uint8
    ) * 255

    for x in range(20, IMAGE_SIZE, 40):
        for y in range(20, IMAGE_SIZE, 40):

            cv2.circle(
                image,
                (x, y),
                8,
                0,
                -1
            )

    return image


def add_damage(image):

    damaged = image.copy()

    # Select an existing photonic-crystal hole
    x = np.random.choice(
        [60, 100, 140]
    )

    y = np.random.choice(
        [60, 100, 140]
    )

    # Remove / modify the original structure
    cv2.circle(
        damaged,
        (x, y),
        np.random.randint(9, 13),
        255,
        -1
    )

    # Add a clearly visible defect
    damage_type = np.random.randint(0, 3)

    if damage_type == 0:

        # Rectangular defect
        width = np.random.randint(10, 19)
        height = np.random.randint(10, 19)

        cv2.rectangle(
            damaged,
            (x - width, y - height),
            (x + width, y + height),
            0,
            -1
        )

    elif damage_type == 1:

        # Irregular defect
        for _ in range(
            np.random.randint(2, 5)
        ):

            dx = np.random.randint(
                -10, 11
            )

            dy = np.random.randint(
                -10, 11
            )

            radius = np.random.randint(
                5, 11
            )

            cv2.circle(
                damaged,
                (x + dx, y + dy),
                radius,
                255,
                -1
            )

    else:

        # Crack-like defect
        points = []

        for k in range(5):

            px = x + np.random.randint(
                -18, 19
            )

            py = y + np.random.randint(
                -18, 19
            )

            points.append(
                [px, py]
            )

        points = np.array(
            points,
            dtype=np.int32
        )

        cv2.polylines(
            damaged,
            [points],
            False,
            255,
            thickness=np.random.randint(2, 5)
        )

    return damaged


print("===================================")
print("CREATING ROBUST PHOTONIC DATASET")
print("===================================")


# Remove old images
for folder in [
    HEALTHY_DIR,
    DAMAGED_DIR
]:

    for filename in os.listdir(folder):

        if filename.endswith(".png"):

            os.remove(
                os.path.join(
                    folder,
                    filename
                )
            )


# Healthy images
for i in range(NUM_IMAGES):

    healthy = create_photonic_crystal()

    cv2.imwrite(
        f"{HEALTHY_DIR}/healthy_{i}.png",
        healthy
    )


# Damaged images
for i in range(NUM_IMAGES):

    healthy = create_photonic_crystal()

    damaged = add_damage(
        healthy
    )

    cv2.imwrite(
        f"{DAMAGED_DIR}/damaged_{i}.png",
        damaged
    )


print(
    f"Healthy images : {NUM_IMAGES}"
)

print(
    f"Damaged images : {NUM_IMAGES}"
)

print(
    "Dataset creation completed. ✅"
)

print("===================================")