import pytest
import pandas as pd

# Sample data for testing
data = [
    ("T001", "U123", 500.00, "USD", "success"),
    ("T002", "U124", -50.00, "EUR", "failed"),
    ("T003", "U125", 0.00, "GBP", "success"),
]

# Allowed currencies
ALLOWED_CURRENCIES = {"USD", "EUR", "GBP"}

# Create DataFrame
df = pd.DataFrame(data, columns=["transaction_id", "user_id", "amount", "currency", "status"])

@pytest.mark.parametrize("amount", df["amount"])
def test_amount_positive(amount):
    """Ensure all amounts are positive."""
    assert amount > 0, f"Invalid amount: {amount}"

@pytest.mark.parametrize("currency", df["currency"])
def test_currency_valid(currency):
    """Ensure all currencies are within the allowed set."""
    assert currency in ALLOWED_CURRENCIES, f"Invalid currency: {currency}"


def test_unique_transaction_id():
    """Ensure there are no duplicate transaction IDs."""
    assert df["transaction_id"].is_unique, "Duplicate transaction IDs found!"