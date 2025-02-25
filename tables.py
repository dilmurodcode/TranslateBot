from config.db import db

User = {
    "telegram_id": "INTEGER NOT NULL",
    "full_name": "VARCHAR(255) NOT NULL",
    "is_superuser": "BOOLEAN DEFAULT 0"
}



if __name__ == "__main__":
    print("Table yaratildi oka 😎")
    db.create_table("User", User)