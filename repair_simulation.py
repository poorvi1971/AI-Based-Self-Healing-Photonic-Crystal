import cv2
import numpy as np
import matplotlib.pyplot as plt


def load_images(
    healthy_path="dynamic_healthy.png",
    damaged_path="dynamic_damaged.png"
):

    healthy = cv2.imread(
        healthy_path,
        cv2.IMREAD_GRAYSCALE
    )

    damaged = cv2.imread(
        damaged_path,
        cv2.IMREAD_GRAYSCALE
    )

    if healthy is None:
        raise FileNotFoundError(healthy_path)

    if damaged is None:
        raise FileNotFoundError(damaged_path)

    return healthy, damaged


def locate_damage_region(
    healthy,
    damaged
):

    difference = cv2.absdiff(
        healthy,
        damaged
    )

    _, mask = cv2.threshold(
        difference,
        30,
        255,
        cv2.THRESH_BINARY
    )

    return mask


def repair_crystal(
    damaged,
    healthy,
    mask
):

    repaired = damaged.copy()

    repaired[mask > 0] = healthy[mask > 0]

    return repaired


def calculate_damage_area(
    mask
):

    return int(
        np.sum(mask > 0)
    )


def calculate_repair_accuracy(
    healthy,
    repaired
):

    matching_pixels = np.sum(
        healthy == repaired
    )

    total_pixels = healthy.size

    return (
        matching_pixels
        / total_pixels
        * 100
    )


def calculate_remaining_error(
    healthy,
    repaired
):

    return int(
        np.sum(healthy != repaired)
    )


def visualize_repair(
    healthy,
    damaged,
    repaired
):

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(
        healthy,
        cmap="gray"
    )
    plt.title("Healthy Crystal")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(
        damaged,
        cmap="gray"
    )
    plt.title("Actual Damaged Crystal")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(
        repaired,
        cmap="gray"
    )
    plt.title("Repaired Crystal")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    print("===================================")
    print("ACTUAL DAMAGE REPAIR SIMULATION")
    print("===================================")

    # Load the SAME dynamic images
    healthy, damaged = load_images()

    # Find actual damaged pixels
    mask = locate_damage_region(
        healthy,
        damaged
    )

    damage_area = calculate_damage_area(
        mask
    )

    print(
        f"Actual damage area: "
        f"{damage_area} pixels"
    )

    # Repair the SAME damaged pixels
    repaired = repair_crystal(
        damaged,
        healthy,
        mask
    )

    # Measure repair
    repair_accuracy = calculate_repair_accuracy(
        healthy,
        repaired
    )

    remaining_error = calculate_remaining_error(
        healthy,
        repaired
    )

    print(
        f"Repair accuracy: "
        f"{repair_accuracy:.2f}%"
    )

    print(
        f"Remaining error: "
        f"{remaining_error} pixels"
    )

    if remaining_error == 0:
        print("Actual damage repaired successfully! ✅")
    else:
        print("Repair incomplete. ⚠️")

    print("===================================")

    cv2.imwrite(
        "dynamic_repaired.png",
        repaired
    )

    print(
        "Repaired image saved as:"
    )
    print(
        "dynamic_repaired.png"
    )

    visualize_repair(
        healthy,
        damaged,
        repaired
    )