#factorial using recursion
def factorial(n):
    if num==0 or num==1:
        return 1
    else:
        return num*factorial(num-1)

num=int(input("Enter the number: "))
if num<0:
    print("Factorial is not defined for -ve no.")
else:
    print("The factorial of",num,"is",factorial(num))