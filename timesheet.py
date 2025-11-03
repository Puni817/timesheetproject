from pymongo import MongoClient
import datetime

# ✅ Step 1: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["timesheet_db"]
collection = db["records"]

# ✅ Step 2: Add Record


def add_record():
    try:
        name = input("Enter employee name: ")
        project = input("Enter project name: ")
        hours = float(input("Enter hours worked: "))
        date = input("Enter date (YYYY-MM-DD): ")

        record = {
            "name": name,
            "project": project,
            "hours": hours,
            "date": date
        }

        collection.insert_one(record)
        print("✅ Record added successfully!\n")
    except Exception as e:
        print("❌ Error adding record:", e)

# ✅ Step 3: View All Records


def view_records():
    print("\n📋 All Timesheet Records:")
    for r in collection.find():
        print(r)
    print()

# ✅ Step 4: Analyze Total Hours by Employee


def analyze_hours():
    print("\n📊 Total Hours Worked by Each Employee:")
    pipeline = [
        {"$group": {"_id": "$name", "total_hours": {"$sum": "$hours"}}}
    ]
    for result in collection.aggregate(pipeline):
        print(f"{result['_id']} - {result['total_hours']} hours")
    print()

# ✅ Step 5: Search Records by Employee


def search_records():
    name = input("Enter employee name to search: ")
    results = collection.find({"name": {"$regex": name, "$options": "i"}})
    print("\n🔍 Matching Records:")
    found = False
    for r in results:
        print(r)
        found = True
    if not found:
        print("❌ No records found.")
    print()

# ✅ Step 6: Update Record by Name + Date


def update_record():
    try:
        name = input("Enter employee name to update: ")
        date = input("Enter the date of the record (YYYY-MM-DD): ")

        record = collection.find_one(
            {"name": {"$regex": name, "$options": "i"}, "date": date})

        if not record:
            print("❌ No record found with that name and date.")
            return

        print("\nExisting Record:")
        print(record)

        print("\nEnter new details (leave blank to keep existing):")
        new_project = input(
            f"Project [{record['project']}]: ") or record['project']
        new_hours = input(f"Hours [{record['hours']}]: ") or record['hours']
        new_date = input(f"Date [{record['date']}]: ") or record['date']

        collection.update_one(
            {"_id": record["_id"]},
            {"$set": {
                "project": new_project,
                "hours": float(new_hours),
                "date": new_date
            }}
        )
        print("✅ Record updated successfully!\n")
    except Exception as e:
        print("❌ Error updating record:", e)

# ✅ Step 7: Delete Record by Name + Date


def delete_record():
    try:
        name = input("Enter employee name to delete: ")
        date = input("Enter date of record (YYYY-MM-DD): ")

        result = collection.delete_one(
            {"name": {"$regex": name, "$options": "i"}, "date": date})
        if result.deleted_count > 0:
            print("🗑️ Record deleted successfully!\n")
        else:
            print("❌ No matching record found.\n")
    except Exception as e:
        print("❌ Error deleting record:", e)

# ✅ Step 8: Menu System


def menu():
    while True:
        print("\n===== 🕒 TIMESHEET MANAGEMENT SYSTEM =====")
        print("1. Add Record")
        print("2. View All Records")
        print("3. Analyze Hours")
        print("4. Search Employee Records")
        print("5. Update Record")
        print("6. Delete Record")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_record()
        elif choice == "2":
            view_records()
        elif choice == "3":
            analyze_hours()
        elif choice == "4":
            search_records()
        elif choice == "5":
            update_record()
        elif choice == "6":
            delete_record()
        elif choice == "7":
            print("👋 Exiting Timesheet Management System. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1-7.")


# ✅ Step 9: Run Program
if __name__ == "__main__":
    menu()
