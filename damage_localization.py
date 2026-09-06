import cv2
import numpy as np


def locate_damage(damaged_path, healthy_path="dataset/healthy/healthy_0.png"):
    damaged = cv2.imread(damaged_path, cv2.IMREAD_GRAYSCALE)
    healthy = cv2.imread(healthy_path, cv2.IMREAD_GRAYSCALE)

    if damaged is None:
        raise FileNotFoundError(f"Could not read: {damaged_path}")

    if healthy is None:
        raise FileNotFoundError(f"Could not read: {healthy_path}")

    # Make sure both images have the same size
    damaged = cv2.resize(damaged, (200, 200))
    healthy = cv2.resize(healthy, (200, 200))

    # Calculate pixel difference
    difference = cv2.absdiff(healthy, damaged)

    # Threshold the difference
    _, mask = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

    # Remove small noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find damaged regions
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask,
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
        return {
            "detected": False,
            "x": None,
            "y": None,
            "area": 0
        }

    x = float(centroids[largest_index][0])
    y = float(centroids[largest_index][1])

    return {
        "detected": True,
        "x": x,
        "y": y,
        "area": int(largest_area)
    }


if __name__ == "__main__":

    result = locate_damage(
        "dataset/damaged/damaged_0.png"
    )

    print("===================================")
    print("DAMAGE LOCALIZATION")
    print("===================================")

    if result["detected"]:
        print("Damage detected!")
        print(f"X coordinate: {result['x']:.2f}")
        print(f"Y coordinate: {result['y']:.2f}")
        print(f"Damage area: {result['area']} pixels")
    else:
        print("No damage detected.")

    print("===================================")