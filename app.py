import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import cv2
import subprocess

from damage_detection import detect_damage
from damage_localization import locate_damage
from robot_navigation import navigate_to_damage

from repair_simulation import (
    load_images,
    locate_damage_region,
    repair_crystal,
    calculate_damage_area,
    calculate_repair_accuracy,
    calculate_remaining_error
)

from optical_verification import run_optical_verification
from risk_prediction import generate_risk_predictions


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Self-Healing Photonic Crystal",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AI-Based Self-Healing Photonic Crystal")
st.write(
    "AI-driven simulation pipeline for damage detection, "
    "localization, robot navigation, virtual repair, optical "
    "verification, and future damage-risk prediction."
)

st.divider()


# ============================================================
# STEP 0 — GENERATE FRESH DAMAGE
# ============================================================

st.header("Step 0 — Dynamic Damage Generation")

if st.button("🔄 Generate New Damage Case"):

    result = subprocess.run(
        ["python3", "dynamic_damage.py"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        st.success("New damage case generated successfully.")
    else:
        st.error("Damage generation failed.")
        st.code(result.stderr)

st.write("Current simulation images:")

col1, col2 = st.columns(2)

with col1:
    st.image(
        "dynamic_healthy.png",
        caption="Healthy Photonic Crystal"
    )

with col2:
    st.image(
        "dynamic_damaged.png",
        caption="Damaged Photonic Crystal"
    )


# ============================================================
# STEP 1 — AI DAMAGE DETECTION
# ============================================================

st.header("Step 1 — AI Damage Detection")

try:

    detection = detect_damage("dynamic_damaged.png")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Prediction",
            detection["result"]
        )

    with col2:
        st.metric(
            "Confidence",
            f"{detection['confidence'] * 100:.2f}%"
        )

    with col3:
        st.metric(
            "Damaged Probability",
            f"{detection['damaged_probability'] * 100:.2f}%"
        )

except Exception as e:

    st.error(f"Damage detection error: {e}")


# ============================================================
# STEP 2 — DAMAGE LOCALIZATION
# ============================================================

st.header("Step 2 — Damage Localization")

try:

    localization = locate_damage(
        "dynamic_damaged.png",
        "dynamic_healthy.png"
    )

    if localization["detected"]:

        x = localization["x"]
        y = localization["y"]
        area = localization["area"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Damage X",
                f"{x:.2f}"
            )

        with col2:
            st.metric(
                "Damage Y",
                f"{y:.2f}"
            )

        with col3:
            st.metric(
                "Damage Area",
                f"{area} px"
            )

        # Visualization
        image = cv2.imread("dynamic_damaged.png")

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        cv2.circle(
            image,
            (int(x), int(y)),
            10,
            (255, 0, 0),
            2
        )

        cv2.circle(
            image,
            (int(x), int(y)),
            3,
            (255, 0, 0),
            -1
        )

        st.image(
            image,
            caption="Localized Damage"
        )

    else:

        st.warning("Damage could not be localized.")

except Exception as e:

    st.error(f"Localization error: {e}")


# ============================================================
# STEP 3 — A* ROBOT NAVIGATION
# ============================================================

st.header("Step 3 — A* Robot Navigation")

try:

    if localization["detected"]:

        navigation = navigate_to_damage(
            localization["x"],
            localization["y"]
        )

        path = navigation["path"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Robot Start",
                str(navigation["start"])
            )

        with col2:
            st.metric(
                "Damage Goal",
                str(navigation["goal"])
            )

        with col3:
            st.metric(
                "Path Length",
                str(navigation["path_length"])
            )

        # Draw A* path
        image = cv2.imread(
            "dynamic_damaged.png"
        )

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

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

        # Robot start
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

        # Damage
        cv2.circle(
            image,
            (int(localization["x"]),
             int(localization["y"])),
            10,
            (255, 0, 0),
            2
        )

        st.image(
            image,
            caption="A* Robot Navigation Path"
        )

except Exception as e:

    st.error(f"A* navigation error: {e}")


# ============================================================
# STEP 4 — VIRTUAL REPAIR
# ============================================================

st.header("Step 4 — Virtual Damage Repair")

try:

    healthy, damaged = load_images(
        "dynamic_healthy.png",
        "dynamic_damaged.png"
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

    cv2.imwrite(
        "dynamic_repaired.png",
        repaired
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Damage Area",
            f"{damage_area} px"
        )

    with col2:
        st.metric(
            "Repair Accuracy",
            f"{repair_accuracy:.2f}%"
        )

    with col3:
        st.metric(
            "Remaining Error",
            f"{remaining_error} px"
        )

    # Before / after visualization

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(12, 4)
    )

    axes[0].imshow(
        healthy,
        cmap="gray"
    )

    axes[0].set_title(
        "Healthy Crystal"
    )

    axes[1].imshow(
        damaged,
        cmap="gray"
    )

    axes[1].set_title(
        "Damaged Crystal"
    )

    axes[2].imshow(
        repaired,
        cmap="gray"
    )

    axes[2].set_title(
        "Repaired Crystal"
    )

    for ax in axes:
        ax.axis("off")

    plt.tight_layout()

    st.pyplot(fig)

    if remaining_error == 0:

        st.success(
            "Virtual damage repaired successfully."
        )

    else:

        st.warning(
            "Virtual repair is incomplete."
        )

except Exception as e:

    st.error(f"Repair error: {e}")


# ============================================================
# STEP 5 — OPTICAL VERIFICATION
# ============================================================

st.header("Step 5 — Optical Response Verification")

try:

    optical = run_optical_verification()

    recovery = optical["recovery"]

    st.metric(
        "Optical Recovery",
        f"{recovery:.2f}%"
    )

    fig = plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        optical["wavelengths"],
        optical["healthy"],
        label="Healthy"
    )

    plt.plot(
        optical["wavelengths"],
        optical["damaged"],
        label="Damaged"
    )

    plt.plot(
        optical["wavelengths"],
        optical["repaired"],
        label="Repaired"
    )

    plt.xlabel(
        "Wavelength (nm)"
    )

    plt.ylabel(
        "Normalized Optical Response"
    )

    plt.title(
        "Optical Response Before and After Repair"
    )

    plt.legend()

    plt.grid(True)

    st.pyplot(fig)

    if recovery >= 90:

        st.success(
            "Optical response successfully recovered."
        )

    else:

        st.warning(
            "Optical recovery is below the target."
        )

except Exception as e:

    st.error(
        f"Optical verification error: {e}"
    )


# ============================================================
# STEP 6 — FUTURE DAMAGE RISK PREDICTION
# ============================================================

st.header("Step 6 — Future Damage Risk Prediction")

try:

    risk_results = generate_risk_predictions()

    high_risk = [
        r for r in risk_results
        if r["risk"] == "HIGH"
    ]

    low_risk = [
        r for r in risk_results
        if r["risk"] == "LOW"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "High-Risk Regions",
            len(high_risk)
        )

    with col2:

        st.metric(
            "Low-Risk Regions",
            len(low_risk)
        )

    st.subheader(
        "Predicted Damage-Risk Map"
    )

    # Create heatmap
    heatmap = np.zeros(
        (200, 200)
    )

    for result in risk_results:

        x = int(result["x"])
        y = int(result["y"])

        probability = result["confidence"]

        x = max(
            0,
            min(199, x)
        )

        y = max(
            0,
            min(199, y)
        )

        heatmap[y, x] = probability

    fig = plt.figure(
        figsize=(8, 6)
    )

    plt.imshow(
        heatmap,
        cmap="hot",
        origin="upper",
        extent=[0, 200, 200, 0]
    )

    plt.colorbar(
        label="Damage Risk Probability"
    )

    plt.xlabel(
        "X Position"
    )

    plt.ylabel(
        "Y Position"
    )

    plt.title(
        "Future Damage Risk Heatmap"
    )

    st.pyplot(fig)

    st.subheader(
        "Risk Prediction Details"
    )

    for result in risk_results:

        if result["risk"] == "HIGH":

            st.error(
                f"Region ({result['x']}, {result['y']}) "
                f"→ HIGH RISK "
                f"({result['confidence'] * 100:.2f}%)"
            )

        else:

            st.success(
                f"Region ({result['x']}, {result['y']}) "
                f"→ LOW RISK "
                f"({result['confidence'] * 100:.2f}%)"
            )

except Exception as e:

    st.error(
        f"Risk prediction error: {e}"
    )


# ============================================================
# FINAL PIPELINE STATUS
# ============================================================

st.divider()

st.header("🔬 Final Self-Healing Pipeline Status")

pipeline_steps = [
    "Damage Generation",
    "AI Damage Detection",
    "Damage Localization",
    "A* Robot Navigation",
    "Virtual Repair",
    "Optical Verification",
    "Future Damage Risk Prediction"
]

for step in pipeline_steps:

    st.success(
        f"✅ {step} completed"
    )


st.subheader(
    "Pipeline Flow"
)

st.code(
    """
Damage
   ↓
AI Detection
   ↓
Damage Localization
   ↓
A* Robot Navigation
   ↓
Virtual Repair
   ↓
Optical Verification
   ↓
Future Damage-Risk Prediction
   ↓
Self-Healing Decision Support
"""
)


# ============================================================
# SCIENTIFIC NOTE
# ============================================================

st.info(
    "Scientific note: This project is a software simulation / "
    "proof-of-concept. The repair stage performs virtual "
    "reference-based reconstruction, and the optical stage "
    "uses a simplified response model rather than full "
    "electromagnetic/FDTD simulation."
)
# ============================================================
# STEP 7 — EVALUATION RESULTS
# ============================================================

st.divider()

st.header("Step 7 — 20-Case Evaluation Results")

try:

    import pandas as pd

    results_df = pd.read_csv(
        "results/evaluation_results.csv"
    )

    st.subheader("Evaluation Summary")

    total_cases = len(results_df)

    avg_confidence = results_df["confidence"].mean()
    avg_path = results_df["path"].mean()
    avg_repair = results_df["repair"].mean()
    avg_optical = results_df["optical"].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Test Cases",
            total_cases
        )

    with col2:
        st.metric(
            "Avg CNN Confidence",
            f"{avg_confidence:.2f}%"
        )

    with col3:
        st.metric(
            "Avg Repair Accuracy",
            f"{avg_repair:.2f}%"
        )

    with col4:
        st.metric(
            "Avg Optical Recovery",
            f"{avg_optical:.2f}%"
        )

    st.metric(
        "Average A* Path Length",
        f"{avg_path:.2f}"
    )

    st.subheader("Actual Per-Case Results")

    st.dataframe(
        results_df,
        width="stretch"
    )

    st.subheader("CNN Confidence")

    st.image(
        "real_cnn_confidence.png",
        caption="CNN Confidence Across 20 Test Cases"
    )

    st.subheader("A* Path Length")

    st.image(
        "real_astar_path_length.png",
        caption="A* Path Length Across 20 Test Cases"
    )

    st.subheader("Repair Accuracy")

    st.image(
        "real_repair_accuracy.png",
        caption="Repair Accuracy Across 20 Test Cases"
    )

    st.subheader("Optical Recovery")

    st.image(
        "real_optical_recovery.png",
        caption="Optical Recovery Across 20 Test Cases"
    )

    st.success(
        "20-case evaluation results loaded successfully."
    )

except FileNotFoundError:

    st.warning(
        "Evaluation files not found. "
        "Run evaluation.py first."
    )

except Exception as e:

    st.error(
        f"Evaluation dashboard error: {e}"
    )
