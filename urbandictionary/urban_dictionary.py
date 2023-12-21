import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('URBAN_DICTIONARY_TOKEN')

base_url = "https://mashape-community-urban-dictionary.p.rapidapi.com"

headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': "mashape-community-urban-dictionary.p.rapidapi.com"
}


async def request_term(term):
    url = base_url + "/define?term=" + term
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data
