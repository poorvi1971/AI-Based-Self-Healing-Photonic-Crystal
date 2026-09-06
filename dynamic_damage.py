import cv2
import numpy as np
import random


IMAGE_SIZE = 200


def create_healthy_crystal():

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


def create_random_damage(image):

    damaged = image.copy()

    # Choose a random crystal location
    x = random.randint(2, 4) * 40
    y = random.randint(2, 4) * 40

    # Remove original hole
    cv2.circle(
        damaged,
        (x, y),
        11,
        255,
        -1
    )

    # Create structural damage
    size = random.randint(14, 20)

    cv2.rectangle(
        damaged,
        (x - size, y - size),
        (x + size, y + size),
        0,
        -1
    )

    # Make damage irregular
    cv2.circle(
        damaged,
        (
            x + random.randint(-8, 8),
            y + random.randint(-8, 8)
        ),
        random.randint(5, 10),
        255,
        -1
    )

    return damaged, (x, y)


if __name__ == "__main__":

    healthy = create_healthy_crystal()

    damaged, location = create_random_damage(
        healthy
    )

    cv2.imwrite(
        "dynamic_healthy.png",
        healthy
    )

    cv2.imwrite(
        "dynamic_damaged.png",
        damaged
    )

    print("===================================")
    print("RANDOM DAMAGE GENERATION")
    print("===================================")

    print(
        f"Damage location: {location}"
    )

    print("Healthy image saved as:")
    print("dynamic_healthy.png")

    print("Damaged image saved as:")
    print("dynamic_damaged.png")

    print("===================================")