# services/report_service.py
from database.database import Database
from datetime import datetime

class ReportService:
    def __init__(self):
        self.db = Database()

    def dashboard(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        data = {}
        cursor.execute("SELECT COUNT(*) FROM customers")
        data["total_customers"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM customers WHERE status='active'")
        data["active_customers"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bills")
        data["total_bills"] = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(amount) FROM payments")
        data["total_income"] = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM bills WHERE status!='paid'")
        data["unpaid_amount"] = cursor.fetchone()[0] or 0
        conn.close()
        return data

    def monthly_report(self, year, month):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as bills, SUM(amount) as total
            FROM bills
            WHERE strftime('%Y', created_at) = ? AND strftime('%m', created_at) = ?
        """, (str(year), f"{month:02d}"))
        result = cursor.fetchone()
        conn.close()
        return {
            "year": year,
            "month": month,
            "bills": result["bills"],
            "amount": result["total"] or 0
        }

    def daily_report(self, date=None):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as bills, SUM(amount) as total
            FROM bills
            WHERE DATE(created_at) = ?
        """, (date,))
        result = cursor.fetchone()
        conn.close()
        return {"date": date, "bills": result["bills"], "amount": result["total"] or 0}

    def block_report(self, block):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(bills.id) as bills, SUM(bills.amount) as total
            FROM bills
            JOIN customers ON bills.customer_id = customers.id
            WHERE customers.block = ?
        """, (block,))
        result = cursor.fetchone()
        conn.close()
        return {"block": block, "bills": result["bills"], "amount": result["total"] or 0}

    def category_report(self, category):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(bills.id) as bills, SUM(bills.amount) as total
            FROM bills
            JOIN customers ON bills.customer_id = customers.id
            WHERE customers.category = ?
        """, (category,))
        result = cursor.fetchone()
        conn.close()
        return {"category": category, "bills": result["bills"], "amount": result["total"] or 0}

    def debt_report(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT customers.name, customers.phone, customers.customer_code,
                   SUM(bills.amount) as debt
            FROM bills
            JOIN customers ON bills.customer_id = customers.id
            WHERE bills.status != 'paid'
            GROUP BY customers.id
            ORDER BY debt DESC
        """)
        debtors = cursor.fetchall()
        conn.close()
        return debtors

    def payment_summary(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT payment_method, SUM(amount) as total
            FROM payments
            GROUP BY payment_method
        """)
        summary = cursor.fetchall()
        conn.close()
        return summary
