import requests

# Function to fetch exchange rate data from a free API (e.g., Open Exchange Rates)
def get_exchange_rates():
    try:
        api_url = "https://api.exchangerate-api.com/v4/latest/USD"  # Replace USD with your base currency
        response = requests.get(api_url)
        data = response.json()
        return data['rates']
    except requests.exceptions.RequestException as e:
        print("Error fetching exchange rates:", e)
        return None

# Function to perform currency conversion
def convert_currency(amount, from_currency, to_currency, exchange_rates):
    try:
        if from_currency == to_currency:
            return amount, 1.0

        from_rate = exchange_rates.get(from_currency)
        to_rate = exchange_rates.get(to_currency)

        if from_rate is None or to_rate is None:
            return None, None

        converted_amount = amount * (to_rate / from_rate)
        return converted_amount, to_rate
    except ZeroDivisionError:
        return None, None

# Function to handle user input
def user_input():
    try:
        amount = float(input("Enter the amount to convert: "))
        from_currency = input("Enter the source currency (e.g., USD): ").upper()
        to_currency = input("Enter the target currency (e.g., EUR): ").upper()

        return amount, from_currency, to_currency
    except ValueError:
        return None, None, None

# Main function
def main():
    exchange_rates = get_exchange_rates()
    
    if exchange_rates is None:
        print("Unable to fetch exchange rates. Please try again later.")
        return
    
    while True:
        amount, from_currency, to_currency = user_input()
        
        if amount is None or from_currency not in exchange_rates or to_currency not in exchange_rates:
            print("Invalid input. Please check your input and try again.")
            continue
        
        converted_amount, exchange_rate = convert_currency(amount, from_currency, to_currency, exchange_rates)
        
        if converted_amount is not None:
            print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
            print(f"Exchange rate used: 1 {from_currency} = {exchange_rate:.4f} {to_currency}")
        
        another_conversion = input("Do you want to perform another conversion? (yes/no): ").lower()
        if another_conversion != 'yes':
            break

if __name__ == "__main__":
    main()
