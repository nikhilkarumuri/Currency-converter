from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Function to fetch exchange rate from Frankfurter API
def get_exchange_rate(base_currency, target_currency):
    try:
        url = f"https://api.frankfurter.app/latest?from={base_currency}&to={target_currency}"
        response = requests.get(url, timeout=5)  # timeout added for safety

        if response.status_code != 200:
            return None

        data = response.json()
        return data['rates'].get(target_currency)

    except requests.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return None

# Route for main page
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            base_currency = request.form['base_currency'].strip().upper()
            target_currency = request.form['target_currency'].strip().upper()
            amount = float(request.form['amount'])

            rate = get_exchange_rate(base_currency, target_currency)
            if rate:
                converted = amount * rate
                result = f"{amount:.2f} {base_currency} = {converted:.2f} {target_currency}"
            else:
                error = "Failed to get exchange rate. Please check currency codes."

        except ValueError:
            error = "Invalid amount entered. Please enter a valid number."
        except Exception as e:
            error = f"Unexpected error: {str(e)}"

    return render_template('index.html', result=result, error=error)

# Run the app in development mode
if __name__ == '__main__':
    app.run(debug=True)

