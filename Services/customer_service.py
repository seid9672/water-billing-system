# services/customer_service.py
from database.database import Database
from datetime import datetime

class CustomerService:
    def __init__(self):
        self.db = Database()

    def create_customer(self, data):
        conn = self.db.connect()
        cursor = conn.cursor()
        customer_code = self.db.generate_customer_code()
        try:
            cursor.execute("""
                INSERT INTO customers(
                    customer_code, name, phone, category, block, zone,
                    house_number, address, meter_number, meter_size
                )
                VALUES(?,?,?,?,?,?,?,?,?,?)
            """, (
                customer_code,
                data.get("name"),
                data.get("phone"),
                data.get("category", "PR"),
                data.get("block"),
                data.get("zone"),
                data.get("house_number"),
                data.get("address"),
                data.get("meter_number"),
                data.get("meter_size")
            ))
            conn.commit()
            customer_id = cursor.lastrowid
            return {"success": True, "customer_id": customer_id, "customer_code": customer_code}
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def get_customer(self, customer_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return customer

    def get_by_code(self, customer_code):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_code = ?", (customer_code,))
        customer = cursor.fetchone()
        conn.close()
        return customer

    def search(self, keyword):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM customers
            WHERE name LIKE ? OR phone LIKE ? OR meter_number LIKE ? OR customer_code LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        results = cursor.fetchall()
        conn.close()
        return results

    def update_customer(self, customer_id, data):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE customers SET
                    name = ?,
                    phone = ?,
                    category = ?,
                    block = ?,
                    zone = ?,
                    house_number = ?,
                    address = ?,
                    meter_number = ?,
                    meter_size = ?,
                    status = ?
                WHERE id = ?
            """, (
                data.get("name"),
                data.get("phone"),
                data.get("category"),
                data.get("block"),
                data.get("zone"),
                data.get("house_number"),
                data.get("address"),
                data.get("meter_number"),
                data.get("meter_size"),
                data.get("status", "active"),
                customer_id
            ))
            conn.commit()
            return {"success": True}
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def delete_customer(self, customer_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            conn.commit()
            return {"success": True}
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def get_history(self, customer_id):
        """የደንበኛ ሙሉ ታሪክ - ንባቦች፣ ቢሎች፣ ክፍያዎች"""
        conn = self.db.connect()
        cursor = conn.cursor()
        # ንባቦች
        cursor.execute("""
            SELECT * FROM meter_readings
            WHERE customer_id = ? ORDER BY reading_date DESC
        """, (customer_id,))
        readings = cursor.fetchall()
        # ቢሎች
        cursor.execute("""
            SELECT * FROM bills
            WHERE customer_id = ? ORDER BY created_at DESC
        """, (customer_id,))
        bills = cursor.fetchall()
        # ክፍያዎች
        cursor.execute("""
            SELECT * FROM payments
            WHERE customer_id = ? ORDER BY payment_date DESC
        """, (customer_id,))
        payments = cursor.fetchall()
        conn.close()
        return {
            "readings": readings,
            "bills": bills,
            "payments": payments
        }

    def total_customers(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        total = cursor.fetchone()[0]
        conn.close()
        return total
