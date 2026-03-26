from services.database import create_tables
from services.logic import (
    create_crop,
    list_crops,
    create_expense,
    list_expenses,
    remove_crop,
    remove_expense,
    show_crop_summary,
    show_expensive_crops,
    clear_all_data,
)


def main():
    create_tables()

    while True:
        print("\n === Farm Manager ===")
        print("1. Add Crop")
        print("2. View Crops")
        print("3. Add Expenses")
        print("4. View Expenses")
        print("5. Delete Crop")
        print("6. Delete Expense")
        print("7. Crop Summary")
        print("8. Show Expensive Crops")
        print("9. CLEAR ALL")
        print("10. Exist")

        choice = input("Choose an option: ")

        if choice == "1":
            create_crop()

        elif choice == "2":
            list_crops()

        elif choice == "3":
            create_expense()

        elif choice == "4":
            list_expenses()

        elif choice == "5":
            remove_crop()

        elif choice == "6":
            remove_expense()

        elif choice == "7":
            show_crop_summary()

        elif choice == "8":
            show_expensive_crops()

        elif choice == "9":
            clear_all_data()

        elif choice == "10":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
