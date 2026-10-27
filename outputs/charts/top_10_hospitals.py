import matplotlib.pyplot as plt

hospitals = [
    "Mount Sinai Hospital",
    "North Shore University Hospital",
    "NY Presbyterian - Columbia",
    "NY Presbyterian - Weill Cornell",
    "Beth Israel Medical Center",
    "Montefiore Medical Center",
    "Strong Memorial Hospital",
    "Long Island Jewish Medical Center",
    "New York Methodist Hospital",
    "Winthrop-University Hospital"
]

patient_counts = [
    3349,
    3017,
    2909,
    2646,
    2595,
    2591,
    2241,
    2219,
    2132,
    2052
]

plt.figure(figsize=(10, 6))

plt.barh(hospitals, patient_counts)

plt.title("Top 10 Hospitals by Patient Count")
plt.xlabel("Number of Patients")
plt.ylabel("Hospital")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("outputs/charts/top_10_hospitals.png")

plt.show()