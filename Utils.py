from datetime import datetime

def date_exists(employee_data, date):
    # Checks if the entered date already exists in the emp history 
    leave_history = employee_data.leave_history
    date_parse = datetime.strptime(date, "%Y-%m-%d").date()
    
    for leave in leave_history:
        if leave.get("status") != "Approved":
            continue
        start = datetime.strptime(leave.get("date"), "%Y-%m-%d").date()
        
        if start == date_parse:
            return True

    return False

def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_yes_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' or 'n'.")
    




