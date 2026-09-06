import subprocess
import re
import statistics
import csv
import json

NUM_CASES = 20

results = []
failed_cases = []

print("\n===================================")
print("20-CASE SELF-HEALING EVALUATION")
print("===================================\n")

for i in range(NUM_CASES):

    print(f"Running case {i + 1}/{NUM_CASES}...")

    subprocess.run(
        ["python3", "dynamic_damage.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    process = subprocess.run(
        ["python3", "main_pipeline.py"],
        capture_output=True,
        text=True
    )

    output = process.stdout + "\n" + process.stderr

    confidence_match = re.search(
        r"Confidence\s*:\s*([\d.]+)\s*%",
        output
    )

    path_match = re.search(
        r"Path Length\s*:\s*(\d+)",
        output
    )

    repair_match = re.search(
        r"Repair Accuracy\s*:\s*([\d.]+)\s*%",
        output
    )

    optical_match = re.search(
        r"Optical Recovery\s*:\s*([\d.]+)\s*%",
        output
    )

    x_match = re.search(
        r"Damage X\s*:\s*([\d.]+)",
        output
    )

    y_match = re.search(
        r"Damage Y\s*:\s*([\d.]+)",
        output
    )

    complete_match = re.search(
        r"SELF-HEALING\s+PIPELINE\s+COMPLETED",
        output,
        re.IGNORECASE
    )

    if not all([
        confidence_match,
        path_match,
        repair_match,
        optical_match,
        x_match,
        y_match,
        complete_match
    ]):
        failed_cases.append(i + 1)
        print(f"  Case {i + 1}: FAILED")
        continue

    confidence = float(confidence_match.group(1))
    path_length = int(path_match.group(1))
    repair = float(repair_match.group(1))
    optical = float(optical_match.group(1))
    x = float(x_match.group(1))
    y = float(y_match.group(1))

    success = (
        confidence >= 50
        and path_length > 0
        and repair >= 99
        and optical >= 95
    )

    if success:

        results.append({
            "case": i + 1,
            "confidence": confidence,
            "path": path_length,
            "repair": repair,
            "optical": optical,
            "x": x,
            "y": y
        })

        print(
            f"  Case {i + 1}: PASS | "
            f"Detection={confidence:.2f}% | "
            f"Path={path_length} | "
            f"Repair={repair:.2f}% | "
            f"Optical={optical:.2f}%"
        )

    else:

        failed_cases.append(i + 1)

        print(
            f"  Case {i + 1}: FAILED | "
            f"Detection={confidence:.2f}% | "
            f"Path={path_length} | "
            f"Repair={repair:.2f}% | "
            f"Optical={optical:.2f}%"
        )


print("\n===================================")
print("FINAL EVALUATION")
print("===================================")

print(
    f"Successful cases : {len(results)}/{NUM_CASES}"
)

print(
    f"Failed cases     : {len(failed_cases)}"
)


if results:

    print("\n===================================")
    print("AVERAGE PERFORMANCE")
    print("===================================")

    print(
        f"Average CNN Confidence : "
        f"{statistics.mean(r['confidence'] for r in results):.2f}%"
    )

    print(
        f"Average A* Path Length : "
        f"{statistics.mean(r['path'] for r in results):.2f}"
    )

    print(
        f"Average Repair Accuracy: "
        f"{statistics.mean(r['repair'] for r in results):.2f}%"
    )

    print(
        f"Average Optical Recovery: "
        f"{statistics.mean(r['optical'] for r in results):.2f}%"
    )


if failed_cases:

    print(
        f"\nFailed case numbers: {failed_cases}"
    )


with open(
    "evaluation_results.csv",
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "case",
            "confidence",
            "path",
            "repair",
            "optical",
            "x",
            "y"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


with open(
    "evaluation_results.json",
    "w"
) as file:

    json.dump(
        results,
        file,
        indent=4
    )


print("\n===================================")
print("EVALUATION COMPLETED")
print("===================================")

print("Actual per-case results saved:")
print("evaluation_results.csv")
print("evaluation_results.json")

print("===================================\n")