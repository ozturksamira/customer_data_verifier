import sqlite3
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class CustomerDataVerifier:
    """Validates and cleans user contact records in a SQLite database."""
    
    def __init__(self, db_path="customers.db"):
        self.db_path = db_path
        # Standard email regex pattern
        self.email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        # Matches E.164 international standard or standard UK/US lengths
        self.phone_regex = re.compile(r"^\+?[1-9]\d{7,14}$")

    def setup_dummy_database(self):
        """Initializes a test database with dirty data for demonstration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    is_valid INTEGER DEFAULT 0
                )
            ''')
            
            # Insert mixed quality data if table is empty
            cursor.execute("SELECT COUNT(*) FROM contacts")
            if cursor.fetchone()[0] == 0:
                dirty_data = [
                    ("Alice Smith", "alice@example.com", "+447449476644"), # Valid
                    ("Bob Jones", "bob@invalid_domain", "07449 476 644"),  # Invalid email, needs phone clean
                    ("Charlie Brown", "charlie.b@domain.co.uk", "12345"),  # Invalid phone
                    ("Diana Prince", "diana@@amazon.com", "N/A"),          # Invalid both
                ]
                cursor.executemany("INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)", dirty_data)
                conn.commit()
                logging.info("Dummy database initialized with test records.")

    def validate_email(self, email):
        """Validates email format using regex."""
        if not email:
            return False
        return bool(self.email_regex.match(email.strip()))

    def validate_and_clean_phone(self, phone):
        """Removes whitespace/dashes and validates phone number length/characters."""
        if not phone:
            return False, None
        
        # Clean the string of spaces, dashes, and parentheses
        clean_phone = re.sub(r"[\s\-\(\)]", "", str(phone))
        
        if self.phone_regex.match(clean_phone):
            return True, clean_phone
        return False, phone

    def process_database(self):
        """Iterates through DB, applies validation logic, and updates records."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, phone FROM contacts")
            records = cursor.fetchall()

            updates = []
            for record_id, name, email, phone in records:
                is_email_valid = self.validate_email(email)
                is_phone_valid, cleaned_phone = self.validate_and_clean_phone(phone)

                # Custom logic: A record is only valid if BOTH email and phone are valid
                is_valid = 1 if (is_email_valid and is_phone_valid) else 0
                
                updates.append((cleaned_phone, is_valid, record_id))
                logging.info(f"Processed {name}: Email Valid={is_email_valid}, Phone Valid={is_phone_valid}")

            # Batch update the database
            cursor.executemany("UPDATE contacts SET phone = ?, is_valid = ? WHERE id = ?", updates)
            conn.commit()
            logging.info("Database verification and cleaning complete.")

if __name__ == "__main__":
    verifier = CustomerDataVerifier()
    verifier.setup_dummy_database()
    verifier.process_database()
