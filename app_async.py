import asyncio
import aiohttp

from bs4 import BeautifulSoup
from parser.apartment_parser import ApartmentParser

user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/86.0.4240.198 Safari/537.36 '
                            'OPR/72.0.3815.465 (Edition Yx GX)'}


async def get_soup(session, url):
    async with session.get(url, headers=user_agent) as resp:
        source = await resp.read()
        soup = BeautifulSoup(source, 'html.parser')
        apartments = soup.find_all('div', class_='search-item')
        for apartment in apartments:
            ApartmentParser(apartment).save_to_postgres()


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for number in range(1, 10):
            url = f'https://www.kijiji.ca/b-apartments-condos/page-{number}/' \
                  f'city-of-toronto/c37l1700273'
            tasks.append(asyncio.ensure_future(get_soup(session, url)))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
