#WAP to calculate the cost of an item in shopping cart with discount based on the total amount of the bill.

n = int(input("Enter the number of items in the cart: "))

total = 0
    
for i in range(n):
    #name = input(f"Enter name of item {i+1}: ")
    price = float(input(f"Enter price of item {i+1}: Rs. "))
    qty = int(input(f"Enter quantity of item {i+1}: "))
    cost = price * qty
    print(f"  Cost for item {i+1}: Rs. {cost:.2f}")
    total += cost

print(f"\nTotal Bill Amount: Rs. {total:.2f}")

# Discount based on total bill
if total >= 5000:
    discount = 20
elif total >= 3000:
    discount = 15
elif total >= 1000:
    discount = 10
elif total >= 500:
    discount = 5
else:
    discount = 0

discount_amount = (discount / 100) * total
final_amount = total - discount_amount

print(f"Discount Applied: {discount}%")
print(f"Discount Amount: Rs. {discount_amount:.2f}")
print(f"Final Amount to Pay: Rs. {final_amount:.2f}")