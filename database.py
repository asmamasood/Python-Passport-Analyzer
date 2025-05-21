import sqlite3

def init_db():
    conn = sqlite3.connect("passports.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        passport_number TEXT UNIQUE,
        country_code TEXT,
        country_name TEXT,
        passport_type TEXT,
        expiry_date TEXT
    )''')
    conn.commit()
    conn.close()

def insert_passport(passport_number, country_code, country_name, passport_type, expiry_date):
    conn = sqlite3.connect("passports.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO passports (passport_number, country_code, country_name, passport_type, expiry_date) VALUES (?, ?, ?, ?, ?)",
                  (passport_number, country_code, country_name, passport_type, expiry_date))
        conn.commit()
        return True, "Passport saved to database."
    except sqlite3.IntegrityError:
        return False, "Passport already exists in database."
    finally:
        conn.close()

def passport_exists(passport_number):
    conn = sqlite3.connect("passports.db")
    c = conn.cursor()
    c.execute("SELECT * FROM passports WHERE passport_number = ?", (passport_number,))
    result = c.fetchone()
    conn.close()
    return result is not None
