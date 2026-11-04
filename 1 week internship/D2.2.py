print("Select operation:")
print("1. Addition (+)")
print("2. Subtraction (-)")
print("3. Multiplication (*)")
print("4. Division (/)")
print("5. Modulus/Remainder (%)")


choice = input("Enter choice (1/2/3/4/5): ")


if choice in ('1', '2', '3', '4', '5'):
    
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    
    if choice == '1':
        result = num1 + num2
        print("Result:", num1, "+", num2, "=", result)

    elif choice == '2':
        result = num1 - num2
        print("Result:", num1, "-", num2, "=", result)

    elif choice == '3':
        result = num1 * num2
        print("Result:", num1, "*", num2, "=", result)

    elif choice == '4':
        if num2 != 0:
            result = num1 / num2
            print("Result:", num1, "/", num2, "=", result)
        else:
            print("Error! Division by zero is not allowed.")

    elif choice == '5':
        if num2 != 0:
            result = num1 % num2
            print("Result:", num1, "%", num2, "=", result)
        else:
            print("Error! Division by zero is not allowed.")

else:
    print("Invalid choice! Please select a valid option from 1 to 5.")