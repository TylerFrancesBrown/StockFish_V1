from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

# Example usage
print(API_KEY)
print(SECRET_KEY)