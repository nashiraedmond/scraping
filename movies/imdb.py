import asyncio
import aiohttp
from dataclasses import dataclass
from aiohttp import ClientSession

# Define a data class to represent the scraped data
@dataclass
class ScrapedData:
    # Define fields for the scraped data
    title: str
    duration: str
    data: str
    rating: str

async def fetch_data(url: str, session: ClientSession) -> ScrapedData:
    async with session.get(url) as response:
        # Parse the response content and extract relevant data
        data = await response.json()
        title = data.get('title', '')
        duration = data.get('duration', '')
        date = data.get('date', '')
        rating = data.get('rating', '')
        
        return ScrapedData(title=title, duration=duration, data=date, rating=rating)


async def scrape_website(urls: list[str]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_data(url, session))
        
        # Execute all tasks asynchronously
        results = await asyncio.gather(*tasks)
        
        # Process the scraped data
        for result in results:
            print(result.title)
            print(result.description)
            print()
            # Process more fields as needed


def main():
    # List of URLs to scrape
    urls_to_scrape = [
        'https://example.com/page1',
        'https://example.com/page2',
        # Add more URLs as needed
    ]
    
    # Run the scraper
    asyncio.run(scrape_website(urls_to_scrape))


if __name__ == "__main__":
    main()


