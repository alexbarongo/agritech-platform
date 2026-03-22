def main():
    crops = []
    expenses = []

    while True:
        print("\n === Farm Manager ===")
        print("1. Add Crop")
        print("2. View Crops")
        print("3. Add Expenses")
        print("4. View Expenses")
        print("5. Delete Crop")
        print("6. Delete Expense")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Crop name: ")
            crops.append(name)
            print("Crop added.")

        elif choice == "2":
            print("\nCrops:")
            for crop in crops:
                print("-", crop)

        elif choice == "3":
            item = input("Expense item: ")
            amount = float(input("Amount: "))
            expenses.append((item, amount))
            print("Expense recorded.")

        elif choice == "4":
            print("\nExpenses:")
            total = 0
            for item, amount in expenses:
                print(f"{item}: {amount}")
                total += amount
                print("Total:", total)

        elif choice == "5":
            print("\nDelete Crop:")
            name = input("Crop to Delete: ")
            if name in crops:
                crops.remove(name)
                # item = name
                expenses.remove((name, amount))
                print(name, "is deleted.")
            else:
                print("Crop not found.")

        elif choice == "6":
            print("\nDelete Expense:")
            item = input("Expense item to be deleted: ")
            amount = float(input("Amount: "))
            if (item, amount) in expenses:
                amount = 0
                expenses.append((item, amount))
                print("Amount is removed, type new amount if present.")
            else:
                print("Expense not found.")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
