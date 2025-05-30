from AI import get_ai_response , generate_ai_reply
from Database import load_employee, save_employee, add_or_edit_employee, log_action
from employee import LeaveRequest
from Utils import date_exists
import json


def main():

    def run_admin():
        print("\n--------------Admin Mode--------------")
        while True:
            choice = input("1. Add/Edit Employee  2. Exit Admin mode \nSelect option: ")
            if choice == "2":
                break
            elif choice == "1":
                add_or_edit_employee()
            else:
                print("Enter options 1 or 2")



    name = input("\n Enter your name: ").lower()
    emp = load_employee(name)

    if not emp:
        print("Employee not found.")
        return
    if emp.is_admin:
        while True:
            Choice = input("\nWould you like to go ahead with \n1. Admin mode  2. Normal mode \nSelect option: ")
            if Choice == "1":
                run_admin()
            elif Choice == "2":
                break
            else:
                print("Enter options 1 or 2")


    print(f"\nWelcome {name}! How can I help you today! Type 'exit' to quit.\n")

    while True:
        user_input = input("\n>>> ")
        if user_input.lower() == "exit":
            break
        
        respons = get_ai_response(user_input)
        #print(respons)
        # convert string reply to json form
        try:
            response = json.loads(respons)
        except json.JSONDecodeError:
            print("Error: AI response is not valid JSON.")
            continue 

        # Extract entities from prompt and store
        intent = response['intent']
        leave_type = response['leave_type']
        start_date = response['start_date']
        day_req = response['days_requested']
        cancel_date = response['cancel_date']

        # When intent is to check balance the corresponding leave type and days are displayed
        if intent == "check_balance":
            if leave_type:
                reply = generate_ai_reply(response,emp,Date_exists=False)
                print("\n" , reply,"\n")
            else:
                print("Please specify the leave type you wish to check the balance of!! (e.g., Annual Leave, Sick Leave, Maternity Leave).")

        # When intent is to request a leave entered date is checked along with the number of days
        elif intent == "request_leave":
            balance = emp.leave_balance.get(leave_type, 0)
            if start_date == None :
                print("Please enter a valid date")
                continue

            Date_exists= date_exists(emp,start_date)
            if day_req > balance or Date_exists:
                reply = generate_ai_reply(response,emp,Date_exists)
                print("\n" , reply,"\n")
                request = LeaveRequest(leave_type, day_req, start_date, "Denied")
                emp.request_leave(request)
            
            if day_req <= balance and Date_exists == False :
                reply = generate_ai_reply(response,emp,Date_exists)
                print("\n" , reply,"\n")
                request = LeaveRequest(leave_type, day_req, start_date, "Approved")
                emp.request_leave(request)
                print("Current all requested leaves:\n")
                for leave in emp.leave_history:
                    if leave.get("status") == "Approved":
                        print(leave)
                    
        # When intent is to cancel a leave it prints the history and cancels corresponding date if it exists
        elif intent == "cancel_leave":
            print("\nCurrent requested leaves:\n")

            for leave in emp.leave_history:
                if leave.get("status") == "Approved":
                    print(leave)

            if not leave_type or not cancel_date:
                print("Please Specify the leave type and date to cancel.")
                continue
            success = emp.cancel_leave(leave_type, cancel_date)
            print(f"Your leave on {cancel_date} has been Cancelled successfully." if success else "No matching leave found.")

        elif intent == "show_history":
            if not emp.leave_history:
                print("Currently no leaves has been requested yet.")
            else:
                for entry in emp.leave_history:
                    print(entry)
        
        save_employee(emp)
        log_action(name, intent, user_input)
        

if __name__ == "__main__":
    main()
