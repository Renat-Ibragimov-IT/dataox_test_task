import asyncio

import aiohttp
from bs4 import BeautifulSoup


class AsyncParser:
    def __init__(self, page_from, page_to, save_to):
        self.page_from = page_from
        self.page_to = page_to
        self.save_to = save_to
        self.user_agent = \
            {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/86.0.4240.198 Safari/537.36 '
                           'OPR/72.0.3815.465 (Edition Yx GX)'}
        self.soup_list = []
        self.run_parser = asyncio.run(
            self.get_tasks(self.page_from, self.page_to))

    async def get_soup(self, url, session):
        async with session.get(url, headers=self.user_agent) as resp:
            source = await resp.read()
            self.soup_list.append(BeautifulSoup(source, 'html.parser'))
            return print(len(self.soup_list))

    async def get_tasks(self, page_from, page_to):
        tasks = []
        sem = asyncio.Semaphore(10)
        async with aiohttp.ClientSession() as session:
            for number in range(page_from, page_to + 1):
                url = f'https://www.kijiji.ca/b-apartments-condos/' \
                      f'page-{number}/city-of-toronto/c37l1700273'
                tasks.append(asyncio.ensure_future(
                    self.bound_fetch(sem, url, session)))
            await asyncio.gather(*tasks)

    async def bound_fetch(self, sem, url, session):
        async with sem:
            await self.get_soup(url, session)


