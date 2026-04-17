#factorial using recursion

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

num = int(input("Enter the number: "))

if num < 0:
    print("Factorial is not defined for -ve no.")
else:
    print("The factorial of", num, "is", factorial(num))