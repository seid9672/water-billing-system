# services/billing_service.py
from database.database import Database
from services.tariff_service import TariffService

class BillingService:
    def __init__(self):
        self.db = Database()
        self.tariff = TariffService()

    def generate_bill(self, customer_id, reading_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meter_readings WHERE id = ?", (reading_id,))
        reading = cursor.fetchone()
        if not reading:
            conn.close()
            return {"success": False, "message": "Reading not found"}
        cursor.execute("SELECT id FROM bills WHERE reading_id = ?", (reading_id,))
        if cursor.fetchone():
            conn.close()
            return {"success": False, "message": "Bill already exists"}
        cursor.execute("SELECT category FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        category = customer["category"] if customer else "PR"
        amount = self.tariff.calculate(reading["consumption"], category)
        invoice = self.generate_invoice()
        cursor.execute("""
            INSERT INTO bills(
                customer_id, reading_id, invoice_number,
                previous_reading, current_reading, consumption, amount
            )
            VALUES(?,?,?,?,?,?,?)
        """, (
            customer_id, reading_id, invoice,
            reading["previous_reading"], reading["current_reading"],
            reading["consumption"], amount
        ))
        conn.commit()
        bill_id = cursor.lastrowid
        conn.close()
        return {
            "success": True,
            "bill_id": bill_id,
            "invoice": invoice,
            "amount": amount
        }

    def generate_invoice(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bills")
        count = cursor.fetchone()[0]
        conn.close()
        return f"INV-{count+1:06d}"

    def get_customer_bills(self, customer_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM bills
            WHERE customer_id = ?
            ORDER BY id DESC
        """, (customer_id,))
        bills = cursor.fetchall()
        conn.close()
        return bills

    def get_bill_by_id(self, bill_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bills WHERE id = ?", (bill_id,))
        bill = cursor.fetchone()
        conn.close()
        return bill

    def get_unpaid_bills(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.*, c.name, c.phone, c.customer_code
            FROM bills b
            JOIN customers c ON b.customer_id = c.id
            WHERE b.status != 'paid'
            ORDER BY b.created_at DESC
        """)
        bills = cursor.fetchall()
        conn.close()
        return bills

    def update_bill_status(self, bill_id, status):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE bills SET status = ? WHERE id = ?", (status, bill_id))
        conn.commit()
        conn.close()
        return True
