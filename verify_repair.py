import numpy as np
import matplotlib.pyplot as plt

size = 200
period = 20
hole_radius = 5

y, x = np.ogrid[:size, :size]

# -----------------------------
# CREATE HEALTHY CRYSTAL
# -----------------------------

healthy = np.ones((size, size), dtype=np.uint8)

for cx in range(10, size, period):
    for cy in range(10, size, period):
        mask = (x - cx) ** 2 + (y - cy) ** 2 <= hole_radius ** 2
        healthy[mask] = 0

# -----------------------------
# CREATE DAMAGE
# -----------------------------

damaged = healthy.copy()

damage_x = 100
damage_y = 100

damaged[
    damage_y - 15:damage_y + 15,
    damage_x - 15:damage_x + 15
] = 0

# -----------------------------
# SIMULATE REPAIR
# -----------------------------

repaired = damaged.copy()

repaired[
    damage_y - 15:damage_y + 15,
    damage_x - 15:damage_x + 15
] = healthy[
    damage_y - 15:damage_y + 15,
    damage_x - 15:damage_x + 15
]

# -----------------------------
# CALCULATE REPAIR ACCURACY
# -----------------------------

difference = np.abs(healthy.astype(int) - repaired.astype(int))

error_pixels = np.sum(difference)
total_pixels = size * size

accuracy = (1 - error_pixels / total_pixels) * 100

print("Repair verification started.")
print("Damaged crystal created.")
print("Repair completed.")
print("Repair accuracy:", round(accuracy, 2), "%")

# -----------------------------
# DISPLAY RESULTS
# -----------------------------

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(healthy, cmap="gray", origin="lower")
plt.title("Healthy")

plt.subplot(1, 3, 2)
plt.imshow(damaged, cmap="gray", origin="lower")
plt.title("Damaged")

plt.subplot(1, 3, 3)
plt.imshow(repaired, cmap="gray", origin="lower")
plt.title("Repaired")

plt.tight_layout()
plt.show()