import numpy as np

from damage_detection import detect_damage
from damage_localization import locate_damage
from robot_navigation import navigate_to_damage
from repair_simulation import (
    load_images,
    locate_damage_region,
    repair_crystal,
    calculate_damage_area,
    calculate_repair_accuracy,
    calculate_remaining_error,
)
from optical_verification import (
    generate_optical_response,
    simulate_damage,
    simulate_repair,
    calculate_optical_recovery,
)


HEALTHY_IMAGE = "dynamic_healthy.png"
DAMAGED_IMAGE = "dynamic_damaged.png"


print("===================================")
print("FINAL PIPELINE")
print("===================================")


# STEP 1 — AI DAMAGE DETECTION
detection = detect_damage(DAMAGED_IMAGE)

print("\nSTEP 1: AI DAMAGE DETECTION")
print("-----------------------------------")
print(f"Result: {detection['result']}")
print(f"Confidence: {detection['confidence'] * 100:.2f}%")
print(f"Damaged probability: {detection['damaged_probability'] * 100:.2f}%")
print(f"Healthy probability: {detection['healthy_probability'] * 100:.2f}%")


# STEP 2 — DAMAGE LOCALIZATION
location = locate_damage(
    DAMAGED_IMAGE,
    HEALTHY_IMAGE
)

print("\nSTEP 2: DAMAGE LOCALIZATION")
print("-----------------------------------")

if not location["detected"]:
    print("Damage location could not be detected.")
    raise SystemExit(1)

damage_x = location["x"]
damage_y = location["y"]

print(f"Damage X: {damage_x:.2f}")
print(f"Damage Y: {damage_y:.2f}")
print(f"Damage Area: {location['area']} pixels")


# STEP 3 — A* ROBOT NAVIGATION
navigation = navigate_to_damage(
    damage_x,
    damage_y
)

print("\nSTEP 3: A* ROBOT NAVIGATION")
print("-----------------------------------")
print(f"Start: {navigation['start']}")
print(f"Goal: {navigation['path'][-1]}")
print(f"Path Length: {navigation['path_length']}")


# STEP 4 — VIRTUAL REPAIR
healthy, damaged = load_images(
    HEALTHY_IMAGE,
    DAMAGED_IMAGE
)

mask = locate_damage_region(
    healthy,
    damaged
)

damage_area = calculate_damage_area(mask)

repaired = repair_crystal(
    damaged,
    healthy,
    mask
)

repair_accuracy = calculate_repair_accuracy(
    healthy,
    repaired
)

remaining_error = calculate_remaining_error(
    healthy,
    repaired
)


print("\nSTEP 4: VIRTUAL REPAIR")
print("-----------------------------------")
print(f"Damage Area: {damage_area} pixels")
print(f"Repair Accuracy: {repair_accuracy:.2f}%")
print(f"Remaining Error: {remaining_error} pixels")


# STEP 5 — OPTICAL VERIFICATION
wavelengths = np.linspace(
    450,
    750,
    300
)

healthy_response = generate_optical_response(
    wavelengths
)

_, damaged_response = simulate_damage(
    wavelengths,
    healthy_response
)

_, repaired_response = simulate_repair(
    wavelengths,
    healthy_response,
    damaged_response
)

optical_recovery = calculate_optical_recovery(
    healthy_response,
    repaired_response
)


print("\nSTEP 5: OPTICAL VERIFICATION")
print("-----------------------------------")
print(f"Optical Recovery: {optical_recovery:.2f}%")

if optical_recovery >= 95:
    print("Optical verification successful! ✅")
else:
    print("Optical recovery below target. ⚠️")


# FINAL STATUS
print("\n===================================")
print("FINAL PIPELINE STATUS")
print("===================================")

if (
    detection["result"] == "DAMAGED"
    and location["detected"]
    and len(navigation["path"]) > 0
    and remaining_error == 0
    and optical_recovery >= 95
):
    print("AI Detection       : PASS ✅")
    print("Localization       : PASS ✅")
    print("A* Navigation      : PASS ✅")
    print("Virtual Repair     : PASS ✅")
    print("Optical Verification: PASS ✅")
    print("-----------------------------------")
    print("SELF-HEALING PIPELINE COMPLETED ✅")
else:
    print("Pipeline completed with warnings. ⚠️")

print("===================================")
