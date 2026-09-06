# AI-Based Self-Healing Photonic Crystal

An AI-driven software simulation and proof-of-concept for autonomous detection, localization, navigation, virtual repair, optical verification, and future damage-risk prediction in a photonic crystal structure.

> **Project type:** Software simulation / proof-of-concept  
> **Physical hardware:** Future work  
> **Current evaluation:** Synthetic photonic-crystal damage

---

## Overview

Photonic crystals are periodic optical structures whose properties depend strongly on their geometry. Damage or structural defects can alter their optical response.

This project explores a closed-loop software architecture for detecting and responding to simulated damage:

**Damage → AI Detection → Localization → A* Navigation → Virtual Repair → Optical Verification → Risk Prediction**

The system combines computer vision, deep learning, path planning, image-based repair simulation, optical-response modeling, and machine learning.

---

## System Workflow

1. Generate a healthy photonic-crystal structure.
2. Introduce simulated structural damage.
3. Use a CNN to classify the crystal as healthy or damaged.
4. Localize the damaged region using image comparison.
5. Calculate a robot path to the damaged region using A*.
6. Simulate repair by restoring damaged pixels from a healthy reference.
7. Verify the repaired structure using a simplified optical-response model.
8. Predict future high-risk regions using a Random Forest model.
9. Evaluate the complete pipeline over multiple synthetic damage cases.

---

## Architecture

```text
                 ┌─────────────────────┐
                 │ Photonic Crystal    │
                 │ Healthy Structure   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Simulated Damage    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ CNN Damage          │
                 │ Detection           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Damage Localization │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ A* Robot Navigation │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Virtual Repair      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Optical Verification│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Future Damage Risk  │
                 │ Prediction          │
                 └─────────────────────┘
Technologies
Python
TensorFlow / Keras
OpenCV
NumPy
Matplotlib
Scikit-learn
Streamlit
A* pathfinding
Convolutional Neural Network
Random Forest
Project Structure
AI_Self_Healing_Photonic_Crystal/
│
├── app.py
├── main_pipeline.py
│
├── photonic_crystal.py
├── create_dataset.py
├── dynamic_damage.py
│
├── damage_detection.py
├── damage_localization.py
├── locate_damage.py
│
├── robot_navigation.py
├── repair_simulation.py
├── optical_verification.py
├── risk_prediction.py
│
├── train_cnn.py
├── damage_detector.keras
│
├── evaluation.py
├── evaluate_cnn.py
├── test_cnn.py
├── verify_repair.py
├── test_pipeline.txt
│
├── generate_real_graphs.py
├── generate_report.py
├── visualization.py
│
├── dataset/
│
├── results/
│   ├── evaluation_results.csv
│   ├── evaluation_results.json
│   ├── real_cnn_confidence.png
│   ├── real_astar_path_length.png
│   ├── real_repair_accuracy.png
│   └── real_optical_recovery.png
│
└── archive/
CNN Damage Detection
The damage detector uses a convolutional neural network trained on synthetic healthy and damaged photonic-crystal images.
CNN Pipeline
Input Image
     ↓
Resize to 100 × 100
     ↓
Convolution
     ↓
Max Pooling
     ↓
Convolution
     ↓
Max Pooling
     ↓
Convolution
     ↓
Max Pooling
     ↓
Dense Layer
     ↓
Dropout
     ↓
Binary Classification
The model predicts healthy/damaged status and reports the corresponding confidence.
Damage Localization
Damage localization is performed by comparing the damaged image with a healthy reference image.
The workflow is:

Healthy Reference
       +
Damaged Image
       ↓
Absolute Difference
       ↓
Thresholding
       ↓
Morphological Processing
       ↓
Connected Components
       ↓
Damage Centroid
The resulting centroid provides an estimated (x, y) damage location.
Robot Navigation
A virtual robot uses the A* pathfinding algorithm to calculate a route from its starting position to the detected damage location.
Robot Start
    ↓
A* Search
    ↓
Shortest Valid Path
    ↓
Damage Location
This represents the navigation layer of a future physical repair system.
Virtual Repair
The current repair stage is a software reconstruction simulation.
The detected damaged pixels are replaced using the corresponding pixels from a healthy reference crystal.

This demonstrates the logic of:

Detect Damage
      ↓
Locate Damage
      ↓
Navigate to Damage
      ↓
Restore Structure
      ↓
Verify Result
The reported repair accuracy therefore represents reference-based image reconstruction, not physical material-repair accuracy.
Optical Verification
The project includes a simplified optical-response model.
The system generates an optical response over a wavelength range and compares:

Healthy Response
       ↓
Damaged Response
       ↓
Repaired Response
       ↓
Optical Recovery
The current optical model is a proof-of-concept representation and is not a full electromagnetic/FDTD simulation.
A future version could integrate an electromagnetic solver such as Meep.

Future Damage-Risk Prediction
A Random Forest classifier is used to estimate future damage risk based on synthetic regional information such as:
Position
Previous damage occurrence
The output classifies regions as:
LOW RISK
HIGH RISK
This provides a predictive-maintenance concept for future autonomous systems.
Evaluation Results
The integrated system was evaluated using 20 independently generated synthetic damage cases.
Final Results
Metric	Result
End-to-end successful cases	20 / 20
End-to-end success rate	100%
Average CNN confidence	99.44%
Average A* path length	21.65
Average virtual repair accuracy	100.00%
Average optical recovery	98.90%
Interpretation
The final evaluation demonstrates that the complete software pipeline successfully completed all tested synthetic damage scenarios.
The results demonstrate software-level feasibility of the proposed closed-loop architecture under simulated conditions.

They do not establish physical repair performance.

Results
The project includes evaluation plots for:
CNN confidence
A* path length
Virtual repair accuracy
Optical recovery
These are available in the results/ directory:
results/
├── real_cnn_confidence.png
├── real_astar_path_length.png
├── real_repair_accuracy.png
└── real_optical_recovery.png
Limitations
The current system is a software simulation / proof-of-concept.
Damage is synthetically generated rather than measured from a physical photonic crystal.
Virtual repair uses a healthy reference image for pixel reconstruction.
Optical verification uses a simplified optical-response model rather than a full electromagnetic/FDTD solver.
A* navigation represents a virtual robot and has not yet been connected to physical robotic hardware.
Future damage-risk prediction is trained on synthetic regional data.
The reported evaluation results demonstrate software-level feasibility under simulated conditions and should not be interpreted as physical repair performance.
Future Work
Integrate a physical photonic-crystal sample.
Add camera or microscope-based real-time inspection.
Connect A* navigation to a physical XY positioning system.
Develop a physical repair mechanism.
Integrate real optical measurement hardware.
Replace the simplified optical model with electromagnetic simulation.
Validate the system using experimentally measured damage and repair data.
Conclusion
This project demonstrates a software-level proof-of-concept for an AI-assisted closed-loop self-healing architecture for photonic-crystal structures.
The current implementation successfully integrates:

Damage Generation → AI Detection → Localization → A* Navigation → Virtual Repair → Optical Verification → Risk Prediction*

The system achieved 20/20 successful synthetic end-to-end evaluations, demonstrating the feasibility of integrating these computational components into a single workflow.

The next major stage is experimental validation using physical hardware and real optical measurements.

