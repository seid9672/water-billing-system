# config.py
# Water Billing System
# Version 5.0


import os


class Config:


    # =============================
    # PROJECT PATH
    # =============================

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )



    # =============================
    # DATABASE
    # =============================

    DATABASE_NAME = os.path.join(

        BASE_DIR,

        "database",

        "water_billing.db"

    )



    # =============================
    # BACKUP
    # =============================

    BACKUP_FOLDER = os.path.join(

        BASE_DIR,

        "backup"

    )


    AUTO_BACKUP = True


    BACKUP_INTERVAL_DAYS = 1


    MAX_BACKUP_FILES = 90





    # =============================
    # COMPANY INFORMATION
    # =============================

    COMPANY_NAME = (
        "Wortej Town Water Supply "
        "and Sewerage Service"
    )


    COMPANY_SHORT_NAME = (
        "Wortej Water"
    )


    REGION = "Amhara"


    ZONE = "South Wollo"


    WOREDA = "Tenta"


    TOWN = "Wortej"





    # =============================
    # TELEGRAM BOT
    # =============================

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")


    ADMIN_IDS = [
        int(x.strip())
        for x in os.getenv("ADMIN_IDS", "357864692").split(",")
        if x.strip().isdigit()
    ]



    BOT_LANGUAGE = "am"





    # =============================
    # API SERVER
    # =============================


    API_HOST = "0.0.0.0"


    API_PORT = 8000


    API_TITLE = (
        "Water Billing System API"
    )


    API_VERSION = "5.0"





    # =============================
    # USER SECURITY
    # =============================


    PASSWORD_MIN_LENGTH = 6


    SESSION_TIMEOUT = 3600


    MAX_LOGIN_ATTEMPTS = 5





    # =============================
    # CUSTOMER SETTINGS
    # =============================


    CUSTOMER_CODE_PREFIX = "WT"


    DEFAULT_CATEGORY = "PR"


    CUSTOMER_STATUS = [

        "active",

        "inactive",

        "disconnected"

    ]





    # =============================
    # TARIFF SETTINGS
    # =============================


    TARIFFS = {


        "PR": [

            {
                "min":0,
                "max":5,
                "price":25
            },

            {
                "min":5,
                "max":10,
                "price":27
            },

            {
                "min":10,
                "max":15,
                "price":28.5
            },

            {
                "min":15,
                "max":25,
                "price":30
            },

            {
                "min":25,
                "max":999999,
                "price":32
            }

        ]

    }





    # =============================
    # BILLING SETTINGS
    # =============================


    BILL_PREFIX = "INV"


    BILL_STATUS = [

        "unpaid",

        "partial",

        "paid",

        "cancelled"

    ]



    PAYMENT_METHODS = [

        "cash",

        "telebirr",

        "bank",

        "mobile"

    ]





    # =============================
    # REPORT SETTINGS
    # =============================


    REPORT_LANGUAGE = "am"


    EXPORT_FORMATS = [

        "xlsx",

        "pdf",

        "csv"

    ]





    # =============================
    # LOGGING
    # =============================


    LOG_FOLDER = os.path.join(

        BASE_DIR,

        "logs"

    )


    LOG_FILE = os.path.join(

        LOG_FOLDER,

        "system.log"

    )