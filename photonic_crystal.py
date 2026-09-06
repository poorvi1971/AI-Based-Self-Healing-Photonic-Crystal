import numpy as np
from PIL import Image
import os

# Dataset folders
os.makedirs("dataset/healthy", exist_ok=True)
os.makedirs("dataset/damaged", exist_ok=True)

size = 200
period = 20
hole_radius = 5

# Create images
for image_number in range(100):

    crystal = np.ones((size, size))

    # Create photonic crystal holes
    for x in range(period // 2, size, period):
        for y in range(period // 2, size, period):

            for i in range(size):
                for j in range(size):

                    distance = np.sqrt(
                        (i - x) ** 2 + (j - y) ** 2
                    )

                    if distance <= hole_radius:
                        crystal[j, i] = 0

    # Save healthy crystal
    image = Image.fromarray((crystal * 255).astype(np.uint8))
    image.save(f"dataset/healthy/healthy_{image_number}.png")

    # Add random damage
    damage_x = np.random.randint(40, 160)
    damage_y = np.random.randint(40, 160)
    damage_radius = np.random.randint(8, 18)

    damaged_crystal = crystal.copy()

    for i in range(size):
        for j in range(size):

            distance = np.sqrt(
                (i - damage_x) ** 2 +
                (j - damage_y) ** 2
            )

            if distance <= damage_radius:
                damaged_crystal[j, i] = 1

    # Save damaged crystal
    damaged_image = Image.fromarray(
        (damaged_crystal * 255).astype(np.uint8)
    )

    damaged_image.save(
        f"dataset/damaged/damaged_{image_number}.png"
    )

print("Dataset created successfully!")
print("100 healthy images")
print("100 damaged images")