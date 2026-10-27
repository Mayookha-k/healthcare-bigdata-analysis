import matplotlib.pyplot as plt

risk_levels = [
    "Minor",
    "Moderate",
    "Major",
    "Extreme"
]

patient_counts = [
    91447,
    32015,
    17009,
    7169
]

plt.figure(figsize=(8, 5))

plt.bar(risk_levels, patient_counts)

plt.title("Patients by Risk of Mortality")
plt.xlabel("Risk of Mortality")
plt.ylabel("Number of Patients")

plt.tight_layout()

plt.savefig("outputs/charts/mortality_risk.png")

plt.show()