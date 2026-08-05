# security/permission.py
class Permission:
    ROLES = {
        "admin": ["all"],
        "manager": ["view_reports", "create_bill", "approve_payment", "view_customers"],
        "cashier": ["receive_payment", "view_bill"],
        "meter_reader": ["add_reading", "view_customer"],
        "viewer": ["view_reports"]
    }

    @staticmethod
    def check(role, action):
        if role not in Permission.ROLES:
            return False
        permissions = Permission.ROLES[role]
        if "all" in permissions:
            return True
        return action in permissions