# services/meter_service.py

from database.database import Database
from datetime import datetime



class MeterService:


    def __init__(self):

        self.db = Database()



    # =========================
    # ADD METER READING
    # =========================


    def add_reading(
            self,
            customer_id,
            current_reading,
            entered_by=None
    ):


        conn = self.db.connect()

        cursor = conn.cursor()



        # Get Last Reading

        cursor.execute("""

        SELECT current_reading

        FROM meter_readings

        WHERE customer_id=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (customer_id,))



        last = cursor.fetchone()



        if last:

            previous = last[
                "current_reading"
            ]

        else:

            previous = 0



        # Validation

        if current_reading < previous:


            conn.close()


            return {

                "success":False,

                "message":
                "Current reading cannot be less than previous reading"

            }





        consumption = (

            current_reading

            -

            previous

        )





        # Duplicate Check

        cursor.execute("""

        SELECT id

        FROM meter_readings

        WHERE customer_id=?

        AND current_reading=?

        """,

        (

            customer_id,

            current_reading

        ))



        duplicate = cursor.fetchone()



        if duplicate:


            conn.close()


            return {


                "success":False,

                "message":
                "Duplicate reading found"

            }





        cursor.execute("""

        INSERT INTO meter_readings(

            customer_id,

            previous_reading,

            current_reading,

            consumption,

            entered_by

        )

        VALUES(?,?,?,?,?)

        """,

        (

            customer_id,

            previous,

            current_reading,

            consumption,

            entered_by

        ))



        conn.commit()



        reading_id = cursor.lastrowid



        conn.close()



        return {


            "success":True,


            "reading_id":
            reading_id,


            "previous":
            previous,


            "current":
            current_reading,


            "consumption":
            consumption


        }





    # =========================
    # READING HISTORY
    # =========================


    def history(
            self,
            customer_id
    ):


        conn=self.db.connect()

        cursor=conn.cursor()



        cursor.execute("""

        SELECT *

        FROM meter_readings

        WHERE customer_id=?

        ORDER BY id DESC

        """,

        (customer_id,))



        data = cursor.fetchall()



        conn.close()



        return data





    # =========================
    # GET LAST READING
    # =========================


    def latest_reading(
            self,
            customer_id
    ):


        conn=self.db.connect()

        cursor=conn.cursor()



        cursor.execute("""

        SELECT *

        FROM meter_readings

        WHERE customer_id=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (customer_id,))



        result = cursor.fetchone()



        conn.close()



        return result





    # =========================
    # APPROVE READING
    # =========================


    def approve_reading(
            self,
            reading_id
    ):


        conn=self.db.connect()

        cursor=conn.cursor()



        cursor.execute("""

        UPDATE meter_readings

        SET approved=1

        WHERE id=?

        """,

        (reading_id,))



        conn.commit()

        conn.close()



        return True
