

import os
import json

DATA_FOLDER = "data"
PASSPORTS_FILE = os.path.join(DATA_FOLDER, "passports.json")

class Passport:
    def __init__(self, number):
        self.number = number

    @staticmethod
    def load_passports():
        if not os.path.exists(PASSPORTS_FILE):
            return {}
        with open(PASSPORTS_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def exists_in_db(passport_number):
        passports = Passport.load_passports()
        return passport_number in passports

    # Optional: Add these if needed
    def is_valid_format(self):
        return self.number.startswith("P<") and 8 <= len(self.number) <= 12

    def masked(self):
        return self.number[:3] + "*" * (len(self.number) - 3)
    
class Passport:
    def __init__(self, number, name=None, expiry=None, country=None):
        self.number = number
        self.name = name
        self.expiry = expiry
        self.country = country
    def masked(self):
        # Example: P<PAK1234567 → P<*******67
        if len(self.number) <= 4:
            return "*" * len(self.number)
        return self.number[:2] + "*" * (len(self.number) - 4) + self.number[-2:]   

    def get_country_code(self):
        
        if len(self.number) >= 5:
            return self.number[1:4]
        return "Unknown"

    def get_country_name(self):
        
        country_map = {
            "PAK": "Pakistan",
            "GBR": "United Kingdom",
            "IND": "India",
            "USA": "United States",
            "CAN": "Canada",
            "AUS": "Australia",
            
        }
        code = self.get_country_code()
        return country_map.get(code, "Unknown")
 

    @staticmethod
    def load_passports():
        if not os.path.exists(PASSPORTS_FILE):
            return {}
        with open(PASSPORTS_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_passports(passports):
        with open(PASSPORTS_FILE, "w") as f:
            json.dump(passports, f, indent=4)

    @staticmethod
    def exists_in_db(passport_number):
        passports = Passport.load_passports()
        return passport_number in passports

    def add_to_db(self):
        passports = self.load_passports()
        if self.number in passports:
            return False, "Passport number already exists."

        passports[self.number] = {
            "name": self.name,
            "expiry": self.expiry,
            "country": self.country
        }
        self.save_passports(passports)
        return True, "Passport added successfully."

