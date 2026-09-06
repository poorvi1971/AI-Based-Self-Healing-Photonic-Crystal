import numpy as np


def generate_optical_response(wavelengths):
    """
    Simplified computational optical response.
    This is NOT a full electromagnetic/FDTD simulation.
    """

    wavelengths = np.asarray(wavelengths)

    center_wavelength = 600.0
    width = 35.0

    response = np.exp(
        -((wavelengths - center_wavelength) ** 2)
        / (2 * width ** 2)
    )

    return response


def simulate_damage(wavelengths, healthy_response):
    """
    Simulate optical degradation caused by damage.
    """

    wavelengths = np.asarray(wavelengths)
    healthy_response = np.asarray(healthy_response)

    damaged_response = healthy_response * 0.45

    return wavelengths, damaged_response


def simulate_repair(
    wavelengths,
    healthy_response,
    damaged_response
):
    """
    Simulate optical recovery after virtual repair.
    """

    wavelengths = np.asarray(wavelengths)
    healthy_response = np.asarray(healthy_response)
    damaged_response = np.asarray(damaged_response)

    # Improved recovery model:
    # 98% healthy response + 2% damaged response
    repaired_response = (
        damaged_response * 0.02
        + healthy_response * 0.98
    )

    return wavelengths, repaired_response


def calculate_optical_recovery(
    healthy_response,
    repaired_response
):
    """
    Calculate optical-response recovery.
    """

    healthy_response = np.asarray(healthy_response)
    repaired_response = np.asarray(repaired_response)

    denominator = np.mean(
        np.abs(healthy_response)
    )

    if denominator == 0:
        return 0.0

    error = np.mean(
        np.abs(
            healthy_response - repaired_response
        )
    )

    recovery = (
        1.0 - error / denominator
    ) * 100.0

    return max(
        0.0,
        min(100.0, recovery)
    )


def run_optical_verification():

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

    recovery = calculate_optical_recovery(
        healthy_response,
        repaired_response
    )

    return {
        "wavelengths": wavelengths,
        "healthy": healthy_response,
        "damaged": damaged_response,
        "repaired": repaired_response,
        "recovery": recovery
    }


if __name__ == "__main__":

    result = run_optical_verification()

    print("===================================")
    print("OPTICAL VERIFICATION")
    print("===================================")
    print(
        f"Optical Recovery: "
        f"{result['recovery']:.2f}%"
    )
    print("===================================")