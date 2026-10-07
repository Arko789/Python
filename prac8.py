#WAP to create update delete elements in a list

lst = []

while True:
    print("\n1.Add  2.View  3.Update  4.Delete  5.Exit")
    choice = int(input("Enter choice: "))
    
    if choice == 1:
        lst.append(input("Enter item: "))
        print("Item added!")

    elif choice == 2:
        if len(lst) == 0:
            print("List is empty!")
        else:
            for i in range(len(lst)):
                print(f"  {i} : {lst[i]}")

    elif choice == 3:
        for i in range(len(lst)):
            print(f"  {i} : {lst[i]}")
        index = int(input("Enter index to update: "))
        if index < len(lst):
            lst[index] = input("Enter new item: ")
            print("Item updated!")
        else:
            print("Invalid index!")

    elif choice == 4:
        for i in range(len(lst)):
            print(f"  {i} : {lst[i]}")
        index = int(input("Enter index to delete: "))
        if index < len(lst):
            print(f"'{lst.pop(index)}' deleted!")
        else:
            print("Invalid index!")

    elif choice == 5:
        print("Exiting!")
        break

    else:
        print("Invalid choice!")