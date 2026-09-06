import numpy as np
from sklearn.ensemble import RandomForestClassifier


def train_risk_model():
    """
    Train a Random Forest model using synthetic historical
    damage examples.

    Features:
    [x_position, y_position, previous_damage_count]

    Target:
    0 = LOW risk
    1 = HIGH risk
    """

    X = np.array([
        [30, 40, 0],
        [70, 80, 3],
        [100, 100, 5],
        [150, 100, 0],
        [180, 140, 4],
        [50, 60, 1],
        [120, 120, 4],
        [160, 60, 1],
        [90, 150, 3],
        [40, 170, 0]
    ])

    y = np.array([
        0, 1, 1, 0, 1,
        0, 1, 0, 1, 0
    ])

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def predict_risk(model, regions):
    """
    Predict future damage risk for crystal regions.
    """

    predictions = []

    for region in regions:

        x, y, previous_damage = region

        probability = model.predict_proba(
            [[x, y, previous_damage]]
        )[0][1]

        risk = (
            "HIGH"
            if probability >= 0.5
            else "LOW"
        )

        predictions.append({
            "x": x,
            "y": y,
            "risk": risk,
            "confidence": probability
        })

    return predictions


def generate_risk_predictions():

    model = train_risk_model()

    regions = [
        [30, 40, 0],
        [70, 80, 3],
        [100, 100, 5],
        [150, 100, 0],
        [180, 140, 4],
        [50, 60, 1],
        [120, 120, 4],
        [160, 60, 1],
        [90, 150, 3],
        [40, 170, 0]
    ]

    return predict_risk(
        model,
        regions
    )


if __name__ == "__main__":

    results = generate_risk_predictions()

    print("===================================")
    print("FUTURE DAMAGE RISK PREDICTION")
    print("===================================")

    for result in results:

        print(
            f"Region ({result['x']}, {result['y']}) "
            f"→ {result['risk']} "
            f"({result['confidence'] * 100:.2f}%)"
        )

    print("===================================")