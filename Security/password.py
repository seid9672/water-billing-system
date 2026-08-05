# security/password.py

import hashlib
import os



def hash_password(password):


    salt = os.urandom(16)



    hashed = hashlib.pbkdf2_hmac(

        "sha256",

        password.encode(),

        salt,

        100000

    )



    return (

        salt.hex()

        +

        ":"

        +

        hashed.hex()

    )





def verify_password(
        password,
        stored_password
):


    try:


        salt, hashed = (
            stored_password.split(":")
        )


        new_hash = hashlib.pbkdf2_hmac(

            "sha256",

            password.encode(),

            bytes.fromhex(salt),

            100000

        )



        return (

            new_hash.hex()

            ==

            hashed

        )


    except:


        return False