from services.database import (
    add_crop,
    add_expense,
    clear_table,
    delete_crop,
    delete_expenses_by_crop,
    get_crops,
    get_expenses_with_crops,
    get_profit_report,
    get_total_expenses_per_crop,
    record_harvest,
)


def create_crop():
    print("\n=== Add New Crop===")

    name = input("Crop name: ").strip()
    if not name:
        print("Crop name cannot be empty!")
        return

    planting_date = input("Planting Date (YYYY-MM-DD) or press Enter to skip: ").strip()

    field_size = input("Field size in acres or press Enter to skip: ").strip()
    try:
        field_size = float(field_size) if field_size else None
    except ValueError:
        print("Invalid field size. Saving as empty.")
        field_size = None

    planted_quantity = input("Quantity planted or press Enter to skip: ").strip()
    try:
        planted_quantity = int(planted_quantity) if planted_quantity else None
    except ValueError:
        print("Invalid quanttity. Saving as empty.")
        planted_quantity = None

    add_crop(name, planting_date, field_size, planted_quantity)
    print(f"{name} added successfully.")


def list_crops():
    crops = get_crops()
    print("\nCrops:")
    for crop in crops:
        crop_id = crop[0] if crop[0] is not None else "Not recorded"
        name = crop[1] if crop[1] is not None else "Not recorded"
        planting_date = crop[2] if crop[2] is not None else "Not recorded"
        field_size = crop[3] if crop[3] is not None else "Not recorded"
        qty_planted = crop[4] if crop[4] is not None else "Not recorded"
        harvest_date = crop[5] if crop[5] is not None else "Not recorded"
        qty_harvested = crop[6] if crop[6] is not None else "Not recorded"
        selling_price = crop[7] if crop[7] is not None else "Not recorded"

        print(
            f"=== Crop {crop_id} === \n"
            f"Name          :{name} \n"
            f"Planting Date :{planting_date} \n"
            f"Field Size    :{field_size} acres \n"
            f"Qty Planted   :{qty_planted} \n"
            f"Harvest Date  :{harvest_date} \n"
            f"Qty Harvested :{qty_harvested} kg \n"
            f"Selling Price :{selling_price}\n"
        )


def create_expense():
    crops = get_crops()

    if not crops:
        print("No crop available.")
        return

    print("\nAvailable Crops:")
    for crop in crops:
        print(f"{crop[0]} - {crop[1]}")

    try:
        crop_id = int(input("Select crop ID: "))
    except ValueError:
        print("Invalid input: Please enter a number")
        return

    selected = get_crop_by_id(crop_id)
    if selected is None:
        print("No crop found with that ID.")
        return

    item = input("Expense item: ")

    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount, please eneter number")
        return

    add_expense(1, item, amount, crop_id)
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

    try:
        crop_id = int(input("Enter crop ID to delete: "))
    except ValueError:
        print("Invalid ID, please enter a number")
        return

    selected = get_crop_by_id(crop_id)
    if selected is None:
        print("No crop found with that ID.")
        return

    delete_crop(int(crop_id))
    print("Crop Deleted.")


def remove_expense():
    list_crops()

    try:
        expense_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Invalid ID, please enter a number")
        return

    selected = get_crop_by_id(expense_id)
    if selected is None:
        print("No crop found with that ID.")
        return

    delete_expenses_by_crop(int(expense_id))
    print("Expenses Deleted.")


def show_crop_summary():
    data = get_total_expenses_per_crop()

    print("\n=== Crop Expense Summary ===")
    for row in data:
        name = row[0]
        total = row[1]
        count = row[2]

        avg = total / count if count != 0 else 0

        print(f"{name} -> Total: {total: .2f} | Entries: {count} | Avg: {avg: .2f}")


def show_expensive_crops():
    data = get_total_expenses_per_crop()
    print("\n=== Expensive Crops Alert ===")

    threshold = float(input("Enter expense threshold: "))

    found = False

    for row in data:
        name = row[0]
        total = row[1]

        if total > threshold:
            print(f"⚠️ {name} is expensive! Total: {total:.2f}")
            found = True

    if not found:
        print("✅ No crops exceed the threshold.")


def get_crop_by_id(crop_id):
    crops = get_crops()
    for crop in crops:
        if crop[0] == crop_id:
            return crop
    return None


def clear_all_data():
    confirm = input("This will DELETE ALL crops and expenses. Type YES to confirm: ")

    if confirm != "YES":
        print("Cancelled.")
        return

    clear_table()
    print("All data has been cleared!")


def show_profit_report():
    data = get_profit_report()

    print("\n=== Profit Report ===")

    for row in data:
        crop_id = row[0]
        name = row[1]
        harvest_qty = row[2]
        selling_price = row[3]
        total_expenses = row[4]
        revenue = row[5]
        profit = row[6]

        status = "PROFIT" if profit > 0 else "LOSS" if profit < 0 else "BREAK EVEN"

        print(
            f"=== {name.capitalize()} ===\n"
            f"Harvest Qty   : {harvest_qty}\n"
            f"Selling Price : {selling_price}\n"
            f"Revenue       : {revenue:.2f}\n"
            f"Expenses      : {total_expenses:.2f}\n"
            f"Profit        : {profit:.2f} ({status})\n"
        )


def add_harvest():
    crops = get_crops()

    if not crops:
        print("No crops available")
        return

    print("\nAvailable Crops:")
    for crop in crops:
        name = crop[1]
        planted = crop[2] if crop[2] is not None else "Not recorded"
        print(f"{crop[0]} - {name} (Planted: {planted})")

    crop_id = input("Enter crop ID to record harvest: ").strip()
    try:
        crop_id = int(crop_id)
    except ValueError:
        print("Invalid ID.")
        return

    harvest_qty = input("Harvest quantity (Kg): ").strip()
    try:
        harvest_qty = float(harvest_qty)
    except ValueError:
        print("Harvest date cannot be empty!")
        return

    harvest_date = input("Harvest date (YYYY-MM-DD): ").strip()
    if not harvest_date:
        print("Harvest date cannot be empty!")
        return

    selling_price = input("Selling Price per Kg: ").strip()
    try:
        selling_price = float(selling_price)
    except ValueError:
        print("Invalid price.")
        return

    record_harvest(crop_id, harvest_qty, harvest_date, selling_price)
    print("Harvest recorded successfully!")
