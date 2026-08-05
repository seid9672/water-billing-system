# main.py
# Water Billing System - Version 5.0

import os
import sys
from config import Config
from database.database import Database
from security.auth_service import AuthService
from bot.bot import main as start_bot

def create_folders():
    folders = [Config.BACKUP_FOLDER, Config.LOG_FOLDER]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def initialize_system():
    print("🚰 Water Billing System")
    print("Starting...")
    
    db = Database()
    
    # ✅ አንድ ጊዜ ብቻ ይጠራል
    db.initialize_database()
    
    if db.check_database():
        print("✅ Database Connected")
    else:
        print("❌ Database Error")
        sys.exit()
    
    # ⚠️ አስወግዱ - ቀድሞ በ initialize_database ውስጥ ተሰርቷል
    # db.insert_default_tariff()
    
    print("✅ Tariff Loaded")

def create_admin():
    auth = AuthService()
    conn = auth.db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    if count == 0:
        auth.create_user(
            username="admin",
            password="admin123",
            full_name="System Administrator",
            role="admin"
        )
        print("✅ Default Admin Created")
        print("Username: admin")
        print("Password: admin123")
    else:
        print("✅ Users Exist")

def main():
    create_folders()
    initialize_system()
    create_admin()
    print()
    print("==========================")
    print("🚰 System Ready")
    print("==========================")
    
    # Start Telegram Bot
    if Config.TELEGRAM_TOKEN and Config.TELEGRAM_TOKEN != "YOUR_BOT_TOKEN_HERE":
        print("🤖 Starting Telegram Bot...")
        start_bot()
    else:
        print("⚠️ Telegram Token Missing")

if __name__ == "__main__":
    main()