#histograpm

import matplotlib.pyplot as plt

marks = [35,45,50,55,60,65,70,75,80,85,90,95]

plt.hist(marks,bins=10,edgecolor = "white")
plt.title("Histogram of Marks")
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.show()