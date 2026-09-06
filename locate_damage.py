import cv2
import numpy as np

image = cv2.imread(
    "dataset/damaged/damaged_0.png",
    cv2.IMREAD_GRAYSCALE
)

if image is None:
    print("Error: image not found.")
    exit()

_, binary = cv2.threshold(
    image,
    50,
    255,
    cv2.THRESH_BINARY_INV
)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
    binary,
    connectivity=8
)

largest_area = 0
largest_index = -1

for i in range(1, num_labels):

    area = stats[i, cv2.CC_STAT_AREA]

    if area > largest_area:
        largest_area = area
        largest_index = i


if largest_index == -1:

    print("No damage detected.")

else:

    center_x = centroids[largest_index][0]
    center_y = centroids[largest_index][1]

    print("Damage detected!")
    print(f"X coordinate: {center_x:.2f}")
    print(f"Y coordinate: {center_y:.2f}")
    print(f"Damage area: {largest_area} pixels")