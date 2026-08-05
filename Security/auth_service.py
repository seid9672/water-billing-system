# security/auth_service.py

from database.database import Database
from security.password import (
    hash_password,
    verify_password
)



class AuthService:


    def __init__(self):

        self.db = Database()



    # =========================
    # CREATE USER
    # =========================


    def create_user(
            self,
            username,
            password,
            full_name,
            role="employee"
    ):


        conn=self.db.connect()

        cursor=conn.cursor()



        password_hash = hash_password(
            password
        )



        cursor.execute("""

        INSERT INTO users(

            username,

            password_hash,

            full_name,

            role

        )

        VALUES(?,?,?,?)

        """,

        (

            username,

            password_hash,

            full_name,

            role

        ))



        conn.commit()

        conn.close()



        return True





    # =========================
    # LOGIN
    # =========================


    def login(
            self,
            username,
            password
    ):


        conn=self.db.connect()

        cursor=conn.cursor()



        cursor.execute("""

        SELECT *

        FROM users

        WHERE username=?

        AND status='active'

        """,

        (username,))



        user=cursor.fetchone()



        conn.close()



        if not user:

            return None



        if verify_password(

            password,

            user["password_hash"]

        ):


            return user



        return None