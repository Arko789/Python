#WAP to generate calendar of a month given the start day and number of days in that month.


st = int(input("Enter the start day of month (1-7, where 1=Sun, 7=Sat): "))
num = int(input("Enter number of days: "))

print(" Sun Mon Tue Wed Thu Fri Sat")
print("----------------------------")

# Print initial blank spaces for padding
for i in range(st - 1):
    print("    ", end="")

# Start counter at the day offset
day_pos = st - 1

# Print days of the month
for day in range(1, num + 1):
    print(f"{day:4d}", end="")
    day_pos += 1
    
    # If Saturday is reached, start a new line
    if day_pos == 7:
        print()
        day_pos = 0

# Print a newline at the end if the last line didn't finish on Saturday
if day_pos != 0:
    print()