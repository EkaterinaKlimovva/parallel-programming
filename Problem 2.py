import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch_google_maps_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.google.ru/maps') as response:
            return await response.text()

async def parse_google_maps_data():
    data = await fetch_google_maps_data()
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.title.string
    print("Title:", title)

async def fetch_and_parse_google_maps_data():
    print("Fetching and Parsing Google Maps data...")
    await parse_google_maps_data()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_and_parse_google_maps_data())

if __name__ == "__main__":
    main()