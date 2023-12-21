import os
import aiohttp
from dotenv import load_dotenv

API_KEY = None

# Try to load the API key from the .env file
try:
    load_dotenv()
    API_KEY = os.getenv('URBAN_DICTIONARY_TOKEN')
except Exception as init_error:
    print(f"Could not initialise Urban Dictionary client: {init_error}")

# Network request related variables
base_url = "https://mashape-community-urban-dictionary.p.rapidapi.com"
headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': "mashape-community-urban-dictionary.p.rapidapi.com"
}


async def request_term(term):
    url = base_url + "/define?term=" + term
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                return data
    except Exception as api_error:
        print(f"An error occurred: {api_error}")
        return None
