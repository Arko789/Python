#Scattered plot

import matplotlib.pyplot as plt
study_hours=[1,2,3,4,5,6,7,8]

marks=[70,75,80,85,90,78,92,88]

plt.scatter(study_hours,marks)

plt.title("Study Hours vs Marks")
plt.xlabel("Study Hours")
plt.ylabel("Marks")
plt.show()