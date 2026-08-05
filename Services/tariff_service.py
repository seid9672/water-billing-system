# services/tariff_service.py

from database.database import Database


class TariffService:


    def __init__(self):

        self.db = Database()



    # =========================
    # BLOCK TARIFF CALCULATION
    # =========================


    def calculate(
            self,
            consumption,
            category="PR"
    ):


        conn = self.db.connect()

        cursor = conn.cursor()



        cursor.execute("""

        SELECT *

        FROM tariffs

        WHERE category=?

        ORDER BY min_unit

        """,

        (category,))



        tariffs = cursor.fetchall()



        conn.close()



        if not tariffs:

            return 0



        amount = 0


        remaining = consumption



        for tariff in tariffs:


            min_unit = tariff["min_unit"]

            max_unit = tariff["max_unit"]

            price = tariff["price"]



            units = min(

                remaining,

                max_unit - min_unit

            )



            if units > 0:


                amount += units * price


                remaining -= units



            if remaining <= 0:

                break



        return amount
