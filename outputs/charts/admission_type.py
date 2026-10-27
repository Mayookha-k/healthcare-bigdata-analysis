import matplotlib.pyplot as plt

admission_types = [
    "Emergency",
    "Elective",
    "Urgent",
    "Newborn",
    "Not Available",
    "Trauma"
]

patient_counts = [
    93337,
    29394,
    12994,
    11617,
    259,
    49
]

plt.figure(figsize=(8, 5))

plt.bar(admission_types, patient_counts)

plt.title("Patients by Type of Admission")
plt.xlabel("Type of Admission")
plt.ylabel("Number of Patients")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig("outputs/charts/admission_type.png")

plt.show()