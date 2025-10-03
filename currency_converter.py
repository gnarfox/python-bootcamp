import requests 


amount = float(input("Enter the amount to convert: "))
from_currency = input("Enter the currency code you want to convert from (e.g., JPY): ").upper()
to_currency = input("Enter the currency code you want to convert to (e.g., USD): ").upper()


# Fetch exchange rates
url = f"https://open.er-api.com/v6/latest/{from_currency}"
response = requests.get(url)
data = response.json()

# Check if the API returned an error
if data['result'] != 'success':
    print("Error fetching exchange rates. Please check the currency code.")
    exit()

# Get the conversion rate
rate = data['rates'].get(to_currency)
if rate is None:
    print("Invalid target currency code.")
    exit()

# Calculate converted amount
converted_amount = amount * rate
print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
