from datetime import datetime
import requests
import random

now = datetime.now()

random_pokemon_id = random.randint(1, 151)

response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random_pokemon_id}")
pokemon = response.json()

print(f"Hello, my name is {pokemon['name']}.")
print(f"Today is {now.strftime('%Y-%m-%d')} and the time is {now.strftime('%H:%M:%S')}.")
