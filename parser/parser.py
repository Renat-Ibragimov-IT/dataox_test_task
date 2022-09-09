import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, \
    NoSuchElementException
from selenium.webdriver.common.by import By
from database import apartments_db, engine

browser = webdriver.Chrome()


for page in range(1, 3):
    try:
        url = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/' \
              f'page-{page}/c37l1700273'
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        apartments = soup.find_all('div', class_='clearfix')
        for apartment in apartments:
            try:
                img_link = apartment.findNext('picture').findNext('img'). \
                    get('data-src')
            except AttributeError:
                img_link = 'Image not found'
            title_text = apartment.findNext('div', class_='title').text.strip()
            try:
                date_posted = datetime.datetime.strptime(
                    apartment.findNext('span',
                                       class_='date-posted').text.strip(),
                    '%d/%m/%Y').strftime('%d-%m-%Y')
            except ValueError:
                date_posted = datetime.datetime.now().strftime('%d-%m-%Y')
            location = apartment.findNext('div', class_='location').find(
                'span'). \
                text.strip()
            bedrooms = apartment.findNext('span',
                                          class_='bedrooms').text.strip(). \
                replace(' ', '').replace('\n', '')
            desc_str = apartment.findNext('div',
                                          class_='description').text.strip()
            description = desc_str[0: desc_str.find("  ")].replace('\n', ' ')
            price = apartment.findNext('div', class_='price').text.strip()[1:]
            if price == 'lease Contact':
                price = 'Unknown'
            currency = apartment.findNext('div', class_='price').text.strip()[
                0]
            if currency == 'P':
                currency = 'Unknown'
            ins = apartments_db.insert().values(
                img_link=img_link, title_text=title_text,
                date_posted=date_posted, location=location, bedrooms=bedrooms,
                description=description, price=price, currency=currency)
            conn = engine.connect()
            r = conn.execute(ins)
        browser.find_element(By.XPATH, '//a[@title="Next"]').click()
    except InvalidSessionIdException as e:
        print(f'PARSING COMPLETED SUCCESSFULLY, {e.msg}')
        browser.close()
    except NoSuchElementException as e:
        print(f'PARSING COMPLETED SUCCESSFULLY {e.msg}')
        browser.close()
