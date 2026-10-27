import matplotlib.pyplot as plt

age_groups = [
    "70 or Older",
    "50 to 69",
    "30 to 49",
    "0 to 17",
    "18 to 29"
]

patient_counts = [
    41670,
    38833,
    31318,
    19940,
    15889
]

plt.figure(figsize=(8, 5))

plt.bar(age_groups, patient_counts)

plt.title("Hospital Patients by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Patients")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig("outputs/charts/age_group_distribution.png")

plt.show()