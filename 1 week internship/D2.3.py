score = float(input("Enter student score (0-100): "))


if score < 0 or score > 100:
    print("Invalid score! Please enter a value between 0 and 100.")
elif score >= 90:
    print("Grade: A+")
elif score >= 80:
    print("Grade: A")
elif score >= 70:
    print("Grade: B")
elif score >= 60:
    print("Grade: C")
elif score >= 50:
    print("Grade: D")
else:
    print("Grade: F (Fail)")