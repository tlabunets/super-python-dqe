import pytest
import requests
from unittest.mock import patch

API_URL = "https://api.marketdata.com/stocks?symbol=AAPL"

# Sample API response
dummy_response = {
    "symbol": "AAPL",
    "price": 145.50,
    "currency": "USD",
    "volume": 2000000
}

@pytest.fixture
def mock_api_response(mocker):
    """Mock API request to return predefined response."""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = dummy_response
    return mock_get


def test_api_status_code(mock_api_response):
    """Ensure API returns 200 OK."""
    response = requests.get(API_URL)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"


def test_api_response_structure(mock_api_response):
    """Ensure API response contains required fields."""
    response = requests.get(API_URL).json()
    required_fields = {"symbol", "price", "currency", "volume"}
    assert required_fields.issubset(response.keys()), "Missing fields in API response!"


def test_price_is_positive(mock_api_response):
    """Ensure the stock price is a positive number."""
    response = requests.get(API_URL).json()
    assert response["price"] > 0, f"Invalid price: {response['price']}"
