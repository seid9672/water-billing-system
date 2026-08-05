# security/audit.py

from database.database import Database



class Audit:


    def __init__(self):

        self.db = Database()



    def log(

        self,

        user_id,

        action,

        table_name,

        record_id,

        description

    ):


        conn=self.db.connect()

        cursor=conn.cursor()



        cursor.execute("""

        INSERT INTO audit_logs(

            user_id,

            action,

            table_name,

            record_id,

            description

        )

        VALUES(?,?,?,?,?)

        """,

        (

            user_id,

            action,

            table_name,

            record_id,

            description

        ))



        conn.commit()

        conn.close()