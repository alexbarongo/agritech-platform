from services.database import (
    create_tables,
    add_crop,
    get_crops,
    add_expense,
    get_expenses,
    delete_crop,
    delete_expenses_by_crop,
)


def main():
    create_tables()
    crops = []
    expenses = []
    amount = 0

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
            add_crop(name)
            print("Crop added.")

        elif choice == "2":
            crops = get_crops()
            for crop in crops:
                print(f"{crop[0]} - {crop[1]}")

        elif choice == "3":
            crops = get_crops()

            if not crops:
                print("No crops available. Please add a crop firts.")
                continue

            print("\nAvailable Crops:")
            for crop in crops:
                print(f"{crop[0]} - {crop[1]}")

            crop_id = int(input("Select crop ID: "))
            item = input("Expense item: ")
            amount = float(input("Amount: "))

            add_expense(item, amount, crop_id)
            print("Expense recorded.")

        elif choice == "4":
            expenses = get_expenses()

            for expense in expenses:
                print(f"{expense[0]} - {expense[1]} - {expense[2]}")

        elif choice == "5":
            crops = get_crops()
            for crop in crops:
                print(f"{crop[0]} - {crop[1]}")
            crop_id = int(input("Enter Crop ID to DELETE: "))
            delete_crop(crop_id)

        elif choice == "6":
            crops = get_crops()

            if not crops:
                print("No crops available. Please add a crop first.")
                continue

            print("\n Crops:")
            for crop in crops:
                print(f"{crop[0]} - {crop[1]}")

            crop_id = int(input("Enter crop ID: "))

            delete_expenses_by_crop(crop_id)
            print("All expenses for crop are deleteed.")

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
