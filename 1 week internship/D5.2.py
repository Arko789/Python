#Line graph

import matplotlib.pyplot as plt

months = ["jan","feb","mar","apr","may","jun"]

sales= [1000,1500,2500,2000,3500]

plt.plot(Months, sales)

plt.xlabel("Months")
plt.ylabel("Sales")
plt.title("Sales Graph")
plt.show()