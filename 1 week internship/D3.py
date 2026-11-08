students = ["Arko", "Rahul", "Priya", "Aman", "Neha"]
marks = [85, 72, 90, 68, 88]
subjects = ("Python", "Mathematics", "Physics")

print("Students:", students)
print("Marks:", marks)
print("Subjects:", subjects)

print("\nFirst three students:", students[:3])
print("Their marks:", marks[:3])

print("\nLast two students:", students[-2:])
print("Their marks:", marks[-2:])

print("\nStudents from index 1 to 3:", students[1:4])
print("Their marks:", marks[1:4])

print("\nAlternate students:", students[::2])
print("Their marks:", marks[::2])

print("\nStudents in reverse order:", students[::-1])
print("Marks in reverse order:", marks[::-1])

print("\nFirst two subjects:", subjects[:2])
print("Subjects in reverse order:", subjects[::-1])