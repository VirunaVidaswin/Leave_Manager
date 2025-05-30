from datetime import datetime, timedelta


class Employee:

    def __init__(self, name, leave_balance, leave_history=None, is_manager=False, is_admin=False):
        self.name = name
        self.leave_balance = leave_balance
        self.leave_history = leave_history or []
        self.is_manager = is_manager
        self.is_admin = is_admin

    def request_leave(self, leave_req):
        # add the leave request to employee history and subtract the days taken

        start = datetime.strptime(leave_req.start_date, "%Y-%m-%d").date()
        added_days = 0
        current = start

        while added_days < leave_req.days:
            if current.weekday() < 5:  # 0–4 = Monday–Friday
                current_date = current.strftime("%Y-%m-%d")
                entry = {
                    "leave_type": leave_req.leave_type,
                    "date": current_date,
                    "status": leave_req.status
                }
                self.leave_history.append(entry)
                added_days += 1
            current += timedelta(days=1)

        if leave_req.status != "Denied":
            self.leave_balance[leave_req.leave_type] -= leave_req.days

    def cancel_leave(self, leave_type, date):
        # sets the status to a date requested to be cancelled

        for req in self.leave_history:
            if req['leave_type'] == leave_type and (req['date'] == date):
                req['status'] = "Cancelled"
                self.leave_balance[leave_type] += 1
                return True
        return False


class LeaveRequest:
    def __init__(self, leave_type, days , start_date, status="Pending"):
        self.leave_type = leave_type
        self.days = days
        self.start_date = start_date
        self.status = status


