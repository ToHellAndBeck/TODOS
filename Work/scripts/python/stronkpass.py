import requests
import cowsay
import random

characters = ["beavis", "cheese", "daemon", "cow", "dragon", "ghostbusters", "kitty", "meow", "milk", "stegosaurus", "stimpy", "turkey", "turtle", "tux"]

def get_strong_password():
    response = requests.get('http://www.dinopass.com/password/strong')
    return response.text.strip()

# List to store passwords

# Generate and save 5 strong passwords to the list
password = get_strong_password()

character = random.choice(characters)

# Print the list of strong passwords
getattr(cowsay, character)(password)

