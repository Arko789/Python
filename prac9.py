#WAP to create a new file and write data into it

filename = input("Enter file name: ")

file = open(filename, "w")

n = int(input("Enter how many lines to write: "))

for i in range(n):
    line = input(f"Enter line {i+1}: ")
    file.write(line + "\n")

file.close()

print(f"\nFile '{filename}' created successfully!")

#read and display the file
file = open(filename, "r")
print("\n------------------------------")
print(f"Data in '{filename}':")
print("------------------------------")
print(file.read())
file.close()