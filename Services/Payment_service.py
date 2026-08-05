# services/payment_service.py
from database.database import Database
from datetime import datetime

class PaymentService:
    def __init__(self):
        self.db = Database()

    def make_payment(self, customer_id, amount, bill_id=None,
                     payment_method="cash", reference_no=None, paid_by=None):
        conn = self.db.connect()
        cursor = conn.cursor()
        receipt = self.generate_receipt()
        cursor.execute("""
            INSERT INTO payments(
                customer_id, bill_id, amount, payment_method,
                reference_no, paid_by
            )
            VALUES(?,?,?,?,?,?)
        """, (customer_id, bill_id, amount, payment_method, reference_no, paid_by))
        payment_id = cursor.lastrowid
        # የቢል ሁኔታ አዘምን
        if bill_id:
            cursor.execute("SELECT amount FROM bills WHERE id = ?", (bill_id,))
            bill = cursor.fetchone()
            if bill:
                cursor.execute("SELECT SUM(amount) FROM payments WHERE bill_id = ?", (bill_id,))
                paid = cursor.fetchone()[0] or 0
                if paid >= bill["amount"]:
                    status = "paid"
                elif paid > 0:
                    status = "partial"
                else:
                    status = "unpaid"
                cursor.execute("UPDATE bills SET status = ? WHERE id = ?", (status, bill_id))
        conn.commit()
        conn.close()
        return {"success": True, "payment_id": payment_id, "receipt": receipt}

    def generate_receipt(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM payments")
        count = cursor.fetchone()[0]
        conn.close()
        return f"RCT-{count+1:06d}"

    def get_payment_history(self, customer_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM payments
            WHERE customer_id = ?
            ORDER BY payment_date DESC
        """, (customer_id,))
        payments = cursor.fetchall()
        conn.close()
        return payments

    def get_unpaid_customers(self):
        """ያልከፈሉ ደንበኞች ዝርዝር (ከቢል ጋር)"""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                c.id, c.customer_code, c.name, c.phone,
                SUM(b.amount) AS total_debt
            FROM customers c
            JOIN bills b ON c.id = b.customer_id
            WHERE b.status != 'paid'
            GROUP BY c.id
            HAVING total_debt > 0
            ORDER BY total_debt DESC
        """)
        customers = cursor.fetchall()
        conn.close()
        return customers

    def get_customer_debt(self, customer_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(amount) FROM bills
            WHERE customer_id = ? AND status != 'paid'
        """, (customer_id,))
        debt = cursor.fetchone()[0] or 0
        conn.close()
        return debt
