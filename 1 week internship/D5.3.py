#pie chart

import matplotlib.pyplot as plt

expenses = [1000,1500,1800,2500]

categories = ["rent","food","travel","entertainment"]

plt.pie(expenses, labels=categories, autopct = "%1.1f")
plt.title("Monthly Expenses")
plt.show()