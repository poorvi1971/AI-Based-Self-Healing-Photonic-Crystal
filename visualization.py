import cv2
import numpy as np


def draw_damage_location(image_path, x, y):
    """
    Draw the detected damage location on the crystal image.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    x = int(round(x))
    y = int(round(y))

    # Outer damage marker
    cv2.circle(
        image,
        (x, y),
        10,
        (255, 0, 0),
        2
    )

    # Center point
    cv2.circle(
        image,
        (x, y),
        3,
        (255, 0, 0),
        -1
    )

    # Label
    cv2.putText(
        image,
        f"Damage ({x}, {y})",
        (x + 10, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 0, 0),
        1,
        cv2.LINE_AA
    )

    return image


def draw_astar_path(
    image_path,
    damage_x,
    damage_y,
    path
):
    """
    Draw the A* robot navigation path.
    
    path contains grid coordinates:
    (row, column)
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if path is None or len(path) == 0:
        return image

    # --------------------------------------------------
    # Draw A* path
    # --------------------------------------------------

    for i in range(1, len(path)):

        r1, c1 = path[i - 1]
        r2, c2 = path[i]

        x1 = c1 * 10 + 5
        y1 = r1 * 10 + 5

        x2 = c2 * 10 + 5
        y2 = r2 * 10 + 5

        cv2.line(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

    # --------------------------------------------------
    # Robot starting point
    # --------------------------------------------------

    start_r, start_c = path[0]

    start_x = start_c * 10 + 5
    start_y = start_r * 10 + 5

    cv2.circle(
        image,
        (start_x, start_y),
        6,
        (0, 0, 255),
        -1
    )

    cv2.putText(
        image,
        "Robot Start",
        (start_x + 8, start_y - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (0, 0, 255),
        1,
        cv2.LINE_AA
    )

    # --------------------------------------------------
    # Damage / goal point
    # --------------------------------------------------

    damage_x = int(round(damage_x))
    damage_y = int(round(damage_y))

    cv2.circle(
        image,
        (damage_x, damage_y),
        10,
        (255, 0, 0),
        2
    )

    cv2.circle(
        image,
        (damage_x, damage_y),
        3,
        (255, 0, 0),
        -1
    )

    cv2.putText(
        image,
        "Damage / Goal",
        (damage_x + 10, damage_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 0, 0),
        1,
        cv2.LINE_AA
    )

    return image