#WAP demonstrating the usage of seek() function in a file

#create and write data into file
file = open("demo.txt", "w")
file.write("Hello World\n")
file.write("I love Python\n")
file.write("BTech CSE 1st Year\n")
file.close()

#open file for reading
file = open("demo.txt", "r")

#read from beginning
print("Reading from beginning:")
print(file.read())

#seek to position 6
file.seek(6)
print("After seek(6) - reading from position 6:")
print(file.read())

file.close()
print("File closed successfully!")