import json
import os
from employee import Employee
from datetime import datetime
from Utils import get_int_input, get_yes_no

File = 'employees.json'

def load_data():
    if not os.path.exists(File):
        return {}
    with open(File, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(File, 'w') as f:
        json.dump(data, f, indent=4)

#Loading current employee details
def load_employee(name):
    data = load_data()
    employees = data.get("employees", {})

    for emp_name in employees:
        if emp_name.lower() == name.lower():
            emp = employees[emp_name]
            return Employee(emp_name, emp["leave_balance"], emp["leave_history"], emp["is_manager"], emp["is_admin"])
        
#Saving or updating employee details
def save_employee(employee):
    data = load_data()
    if "employees" not in data:
        data["employees"] = {}

    data["employees"][employee.name] = {
        "leave_balance": employee.leave_balance,
        "leave_history": employee.leave_history,
        "is_manager": getattr(employee, "is_manager", False),
        "is_admin": getattr(employee, "is_admin", False)
    }
    save_data(data)

#unction for admin role to edit current or add a new employee
def add_or_edit_employee():
    name = input("\nEnter new or existing Employee Name: ").title()
    data = load_data()

    if "employees" not in data:
        data["employees"] = {}

    # Check if employee already exists
    emp_name = load_employee(name)
    if emp_name is not None:
        print(f"\n{name} already exists.")
        choice = input("\nDo you want to update their details? (y/n): ").lower()
        if choice != 'y':
            print("No changes made.\n")
            return
        # Show current leave balances
        print(f"\nCurrent Leave Balance: {emp_name.leave_balance}\n")
    else:
        print(f"\nAdding new employee: {name}\n")

    # updated or new data
    is_mgr = get_yes_no("\nIs Manager? (y/n): ")
    is_admin = get_yes_no("\nIs Admin? (y/n): ")
    sick = get_int_input("\nNumber of Sick Leaves: ")
    annual = get_int_input("\nNumber of Annual Leaves: ")
    maternity = get_int_input("\nNumber of Maternity Leaves: ")

    leave_balance = {
        "Sick Leave": sick,
        "Annual Leave": annual,
        "Maternity Leave": maternity
    }

    # Preserve old leave history 
    leave_history = data["employees"][name]["leave_history"] if name in data["employees"] else []

    emp = Employee(name, leave_balance, leave_history, is_mgr, is_admin)
    save_employee(emp)
    print(f"\n{name}'s record has been {'updated successfully' if name in data['employees'] else 'created and saved successfully'}.\n")


#Function to log all user activity
def log_action(user, intent, msg):
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} | {user} | {intent} | {msg}\n")

