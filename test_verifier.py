import pytest
from verifier import CustomerDataVerifier

@pytest.fixture
def verifier():
    # Initializes the class without writing to a permanent database file for tests
    return CustomerDataVerifier(db_path=":memory:")

# --- EMAIL VALIDATION TESTS ---
def test_valid_emails(verifier):
    assert verifier.validate_email("ozturk05samira@gmail.com") is True
    assert verifier.validate_email("user.name+tag@domain.co.uk") is True

def test_invalid_emails(verifier):
    assert verifier.validate_email("plainaddress") is False
    assert verifier.validate_email("@missingusername.com") is False
    assert verifier.validate_email("user@.com") is False
    assert verifier.validate_email("") is False

# --- PHONE VALIDATION & CLEANING TESTS ---
def test_valid_and_dirty_phones(verifier):
    # Standard format
    is_valid, phone = verifier.validate_and_clean_phone("+447449476644")
    assert is_valid is True
    assert phone == "+447449476644"

    # Dirty format (contains spaces and dashes)
    is_valid, phone = verifier.validate_and_clean_phone("+44 (0) 7449-476-644")
    assert is_valid is True
    assert phone == "+4407449476644"

def test_invalid_phones(verifier):
    is_valid, _ = verifier.validate_and_clean_phone("123") # Too short
    assert is_valid is False

    is_valid, _ = verifier.validate_and_clean_phone("invalid_phone") # Letters
    assert is_valid is False
