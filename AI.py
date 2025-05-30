from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()  # Load variables from .env
client = OpenAI()


def get_ai_response(user_input):
    prompt = f"""
    
    You are a leave management assistant. Extract the intent and entities from the user input.
    Normalize plural or lowercase leave types to match: "Annual Leave", "Sick Leave", or "Maternity Leave".
    The leave_type should be extracted even if the user types it in plural or lowercase form e.g., "annual leaves", "sick leaves", maternity leaves.
    If the user says "my [type] leave", extract the leave_type correctly.
    Always normalize variants like "annual leaves", "my sick leave", or "maternity leaves" to: "Annual Leave", "Sick Leave", or "Maternity Leave".
    
    
    Return a JSON object with keys:
    - intent: one of ["check_balance", "request_leave", "cancel_leave", "show_history"]
    - leave_type: normalized to one of ["Annual Leave", "Sick Leave", "Maternity Leave"]
    - days_requested: number of days mentioned (integer)
    - start_date: in format 2025-MM-DD ( Year should always be 2025)
    - cancel_date: if relevant, else null


    Example:
    User input: "I need 3 sick leaves starting from 2025-03-15."
    JSON output:
    {{
    "intent": "request_leave",
    "leave_type": "Sick Leave",
    "days_requested": 3,
    "start_date": "2025-03-15",
    "cancel_date": null
    }}

    User input: "{user_input}"
    JSON output:
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts leave management intents and entities."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    # Extract JSON text from response
    content = response.choices[0].message.content.strip()
    return content


def generate_ai_reply(parsed_data, employee_data, date_exists):
    prompt = f"""
    You are a friendly and helpful HR leave management assistant. Based on the extracted data below, generate a natural-sounding reply to the employee.

    ### Extracted Data:
    intent: {parsed_data.get("intent")}
    leave_type: {parsed_data.get("leave_type")}
    days_requested: {parsed_data.get("days_requested")}
    start_date: {parsed_data.get("start_date")}
    cancel_date: {parsed_data.get("cancel_date")}

    ### Employee Data:
    remaining_balance: {employee_data.leave_balance.get(parsed_data.get("leave_type"), 0)}
    Reuested_Leaves_History: {employee_data.leave_history}

    ### Rules:
    - Do NOT include greetings like "Hello!" or sign-offs like "Best regards!".
    - If intent is "check_balance", respond with how many days of that leave type the employee has.
    - If intent is "request_leave":
    - If days_requested > remaining_balance, politely reject and mention available days.
    - If {date_exists} is equal to True, politely reject and mention to select different date as mentioned date already exists.
    - If enough balance, confirm request and repeat back the leave period.
    - If intent is "cancel_leave", confirm cancellation for the specific date.
    - If intent is "show_history", summarize or mention that the leave history is being displayed.

    Respond in a helpful and polite tone. Do not output JSON. Just write the message you would send to the employee.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant responding to leave management queries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()
