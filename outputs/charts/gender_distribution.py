import matplotlib.pyplot as plt

genders = ["Female", "Male", "Unknown"]
patient_counts = [83021, 64628, 1]

plt.figure(figsize=(7, 5))

plt.bar(genders, patient_counts)

plt.title("Hospital Patients by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Patients")

plt.tight_layout()

plt.savefig("outputs/charts/gender_distribution.png")

plt.show()