from selenium import webdriver
from bs4 import BeautifulSoup
import datetime


browser = webdriver.Chrome()
browser.get('https://www.kijiji.ca/b-apartments-condos/'
            'city-of-toronto/c37l1700273')
soup = BeautifulSoup(browser.page_source, "html.parser")

apartments = soup.find_all('div', class_='clearfix')
count = 0
for apartment in apartments:
    img_link = apartment.findNext('picture').findNext('img').get('data-src')
    title_text = apartment.findNext('div', class_='title').text.strip()
    try:
        date_posted = datetime.datetime.strptime(
            apartment.findNext('span', class_='date-posted').text.strip(),
            '%d/%m/%Y').strftime('%d-%m-%Y')
    except ValueError:
        date_posted = datetime.datetime.now().strftime('%d-%m-%Y')
    location = apartment.findNext('div', class_='location').find('span').\
        text.strip()
    bedrooms = apartment.findNext('span', class_='bedrooms').text.strip().\
        replace(' ', '').replace('\n', '')
    desc_str = apartment.findNext('div', class_='description').text.strip()
    description = desc_str[0: desc_str.find("  ")].replace('\n', ' ')
    price = apartment.findNext('div', class_='price').text.strip()[1:]
    if price == 'lease Contact':
        price = 'Unknown'
    currency = apartment.findNext('div', class_='price').text.strip()[0]
    if currency == 'P':
        currency = 'Unknown'
    count += 1
    print(f'APARTMENT # {count}: [{img_link}, {title_text}, {date_posted}, {location},'
          f' {bedrooms}, {description}, {price}, {currency}]')



