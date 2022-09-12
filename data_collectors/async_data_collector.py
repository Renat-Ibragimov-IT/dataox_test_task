import asyncio

import aiohttp
from bs4 import BeautifulSoup

from parser.apartment_parser import ApartmentParser
from parser.logger_conf import logger


class AsyncDataCollector:
    """
    Class of data collector using asynchronous operation scheme.
    """

    def __init__(self, page_from, page_to, save_to):
        """
        Method to initiate class instance, start data collection and run
        parser by calling parser object. All parameters receiving from
        CLI app arguments.
        Parameters
        __________
        page_from : int
            Specified the site page to start parsing.
        page_to : int
            Specified the site page to end parsing.
        save_to : str
            Specified how the data will be saved.
        """
        self.page_from = page_from
        self.page_to = page_to
        self.save_to = save_to
        self.user_agent = \
            {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/86.0.4240.198 Safari/537.36 '
                           'OPR/72.0.3815.465 (Edition Yx GX)'}
        self.soup = []
        self.run_collector(self.page_from, self.page_to)
        ApartmentParser(self.soup, self.save_to)

    async def get_soup(self, url: str, session, page_number: int):
        """
        Method to collect html data from website page and save to the list for
        future use.
        Parameters
        __________
        url : str
            URL address of page for data collecting.
        session
            Aiohttp ClientSession object.
        page_number : str
            Number of working page. Using for logging.
        """
        async with session.get(url, headers=self.user_agent) as resp:
            source = await resp.read()
            self.soup.append(BeautifulSoup(source, 'html.parser'))
            logger(f'Page # {page_number} parsed')

    async def get_tasks(self, page_from: int, page_to: int):
        """
        Method to collect async tasks
        Parameters
        __________
        page_from : int
            Specified the site page to start parsing.
        page_to : int
            Specified the site page to end parsing.
        """
        tasks = []
        sem = asyncio.Semaphore(10)
        async with aiohttp.ClientSession() as session:
            for number in range(page_from, page_to + 1):
                url = f'https://www.kijiji.ca/b-apartments-condos/' \
                      f'page-{number}/city-of-toronto/c37l1700273'
                tasks.append(asyncio.ensure_future(
                    self.bound_fetch(sem, url, session, number)))
            await asyncio.gather(*tasks)

    async def bound_fetch(self, sem, url: str, session, page_number: int):
        """
        Method for using asyncio.Semaphore object.
        Parameters
        __________
        sem
            asyncio.Semaphore object.
        url : str
            URL address of page for data collecting.
        session
            Aiohttp ClientSession object.
        page_number : str
            Number of working page. Using for logging.
        """
        async with sem:
            await self.get_soup(url, session, page_number)

    def run_collector(self, page_from: int, page_to: int):
        """
        Method to run async data collector.
        Parameters
        __________
        page_to : int
            Specified the site page to end parsing.
        save_to : str
            Specified how the data will be saved.
        """
        asyncio.run(self.get_tasks(page_from, page_to))
