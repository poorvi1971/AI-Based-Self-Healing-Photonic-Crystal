import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("evaluation_results.csv")

print("===================================")
print("GENERATING REAL EVALUATION GRAPHS")
print("===================================")

# CNN Confidence
plt.figure(figsize=(9, 5))
plt.plot(
    df["case"],
    df["confidence"],
    marker="o"
)
plt.xlabel("Test Case")
plt.ylabel("CNN Confidence (%)")
plt.title("CNN Damage Detection Confidence")
plt.grid(True)
plt.tight_layout()
plt.savefig("real_cnn_confidence.png", dpi=300)
plt.close()


# A* Path Length
plt.figure(figsize=(9, 5))
plt.plot(
    df["case"],
    df["path"],
    marker="o"
)
plt.xlabel("Test Case")
plt.ylabel("A* Path Length")
plt.title("A* Robot Navigation Path Length")
plt.grid(True)
plt.tight_layout()
plt.savefig("real_astar_path_length.png", dpi=300)
plt.close()


# Repair Accuracy
plt.figure(figsize=(9, 5))
plt.plot(
    df["case"],
    df["repair"],
    marker="o"
)
plt.xlabel("Test Case")
plt.ylabel("Repair Accuracy (%)")
plt.title("Virtual Repair Accuracy")
plt.grid(True)
plt.tight_layout()
plt.savefig("real_repair_accuracy.png", dpi=300)
plt.close()


# Optical Recovery
plt.figure(figsize=(9, 5))
plt.plot(
    df["case"],
    df["optical"],
    marker="o"
)
plt.xlabel("Test Case")
plt.ylabel("Optical Recovery (%)")
plt.title("Optical Response Recovery")
plt.grid(True)
plt.tight_layout()
plt.savefig("real_optical_recovery.png", dpi=300)
plt.close()


print()
print("REAL GRAPHS GENERATED ✅")
print()
print("real_cnn_confidence.png")
print("real_astar_path_length.png")
print("real_repair_accuracy.png")
print("real_optical_recovery.png")
print("===================================")