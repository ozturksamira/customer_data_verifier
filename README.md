# Customer Data Verification Engine

An automated backend utility designed to validate, clean, and standardize user contact records within a relational database. This project demonstrates data processing and sanitation capabilities, utilizing regular expressions for custom validation logic and an automated test suite to ensure application robustness and zero runtime exceptions.

## Core Features

*   **Automated Data Cleaning:** Sanitizes dirty phone numbers by stripping invalid characters (spaces, dashes, parentheses) and formatting them to standard lengths before committing them back to the database.
*   **Regex Validation:** Implements strict regular expression patterns to evaluate whether emails and phone numbers meet expected international structural formats.
*   **SQLite Integration:** Connects to a SQLite database to ingest raw user records, evaluates their validity against the custom logic rules, and batch-updates the database with the cleaned data and boolean validation flags.
*   **Zero-Exception Testing:** Features a comprehensive `pytest` suite designed to verify edge cases, invalid inputs, and formatting rules without interacting with the production database.

## Tech Stack

*   **Language:** Python 3.x
*   **Database:** SQLite3
*   **Testing Framework:** PyTest
*   **Core Libraries:** `re` (Regular Expressions), `logging`

## Execution Workflow

1.  **Ingestion:** The script queries the `contacts` table to retrieve all raw user records.
2.  **Email Validation:** Evaluates the email string against a standard user/domain regex pattern.
3.  **Phone Sanitation:** Strips non-numeric characters from the phone string, then evaluates the remaining digits against standard length requirements.
4.  **Batch Update:** Determines a final `is_valid` boolean based on the combined validation results and executes a batch `UPDATE` query to overwrite the dirty data with the sanitized values.

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/customer-data-verifier.git](https://github.com/YourUsername/customer-data-verifier.git)
   cd customer-data-verifier
   ```

2. **Install testing dependencies:**
   ```bash
   pip install pytest
   ```

3. **Run the automated test suite:**
   Execute the unit tests to verify the regex and validation logic.
   ```bash
   pytest test_verifier.py -v
   ```

4. **Run the verification engine:**
   Executing the main script will generate a dummy SQLite database, populate it with dirty test data, and process the records.
   ```bash
   python verifier.py
   ```

## License
This project is licensed under the MIT License.
