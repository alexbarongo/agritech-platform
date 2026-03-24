from services.database import (
    add_crop,
    get_crops,
    add_expense,
    get_expenses_with_crops,
    delete_crop,
    delete_expenses_by_crop,
)


def create_crop():
    name = input("Crop name: ")
    add_crop(name)
    print("Crop added.")


def list_crops():
    crops = get_crops()
    print("\nCrops:")
    for crop in crops:
        print(f"{crop[0]} - {crop[1]}")


def create_expense():
    crops = get_crops()

    if not crops:
        print("No crop available.")
        return

    print("\nAvailable Crops:")
    for crop in crops:
        print(f"{crop[0]} - {crop[1]}")

    crop_id = input("Select crop iD: ")
    item = input("Expense item: ")

    try:
        amount = float(input("Amount: "))
    except:
        print("Invalid amount")
        return

    add_expense(item, amount, crop_id)
    print("Expenses recorderd.")


def list_expenses():
    expenses = get_expenses_with_crops()
    total = 0

    print("\nExpenses:")
    for exp in expenses:
        print(f"{exp[1]} -> {exp[2]}: {exp[3]}")
        total += exp[3]

        print("Total:", total)


def remove_crop():
    list_crops()
    crop_id = input("Enter crop ID to delete: ")

    if not crop_id.isdigit():
        print("Invalid ID")
        return

    delete_crop(int(crop_id))
    print("Crop Deleted.")


def remove_expense():
    list_crops()
    expense_id = input("Enter expense ID to delete: ")

    if not expense_id.isdigit():
        print("Invalid ID")
        return

    delete_expenses_by_crop(int(expense_id))
    print("Expenses Deleted.")
