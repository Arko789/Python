#Bar chart

import matplotlib.pyplot as plt

studetns = ["john","Alice","Bob","Eve"]

marks = [85, 92, 78, 95]


plt.bar(students,marks)

plt.xlabel("Student names")
plt.ylabel("Marks")
plt.title("Student Marks")
plt.show()