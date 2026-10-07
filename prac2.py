# WAP to find Total, Average, Percentage and Grade of a Student

n = int(input("Enter the number of subjects: "))
m = int(input("Enter the maximum marks possible for one subject: "))
max_marks = n * m
t_marks=0


for i in range(n):
    marks = float(input(f"Enter marks for subject {i+1}: "))
    t_marks += marks

average = t_marks / n
percentage = (t_marks / max_marks) * 100

if percentage >= 90:
    grade = "A"
elif percentage >= 80:
    grade = "B"
elif percentage >= 70:
    grade = "C"
elif percentage >= 60:
    grade = "D"
elif percentage >= 40:
    grade = "E"
else:
    grade = "F"

# Display result
print(f"Total Marks: {t_marks}")
print(f"Average Marks: {average:.2f}")
print(f"Percentage: {percentage:.2f}%")
print(f"Grade: {grade}")
