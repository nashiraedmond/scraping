import asyncio
import aiohttp
from dataclasses import dataclass
from aiohttp import ClientSession

# Define a data class to represent the scraped data
@dataclass
class RedditPost:
    title: str
    author: str
    subreddit: str
    url: str

async def fetch_data(search_query: str, session: ClientSession) -> list[RedditPost]:
    url = f"https://www.reddit.com/search.json?q={search_query}"
    async with session.get(url) as response:
        # Parse the response content and extract relevant data
        data = await response.json()
        posts = data.get('data', {}).get('children', [])
        reddit_posts = []
        for post in posts:
            post_data = post.get('data', {})
            title = post_data.get('title', '')
            author = post_data.get('author', '')
            subreddit = post_data.get('subreddit', '')
            url = post_data.get('url', '')
            reddit_posts.append(RedditPost(title=title, author=author, subreddit=subreddit, url=url))
        return reddit_posts

async def scrape_reddit(search_query: str):
    async with aiohttp.ClientSession() as session:
        reddit_posts = await fetch_data(search_query, session)
        for post in reddit_posts:
            print(f"Title: {post.title}")
            print(f"Author: {post.author}")
            print(f"Subreddit: {post.subreddit}")
            print(f"URL: {post.url}")
            print()

def main():
    search_query = "python"  # Change the search query here
    asyncio.run(scrape_reddit(search_query))

if __name__ == "__main__":
    main()
