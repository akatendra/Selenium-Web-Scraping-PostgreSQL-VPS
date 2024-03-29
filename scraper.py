from datetime import timedelta, datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from bs4 import BeautifulSoup
import logging
import logging.config


from fake_useragent import UserAgent
# from selenium_stealth import stealth
import undetected_chromedriver as uc
import database

# from config_local import path_chromedriver, path_geckodriver, headless_mode
from config_vps import path_chromedriver, path_geckodriver, headless_mode

# Global variables
vtorichka_counter = 0
novostroy_counter = 0
doma_dachi_kottedzhi_counter = 0
user_agent = UserAgent()

# Set up logging
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
# Remove from output to the log information from Firefox, where a lot
# of space is taken up by the server response with the html content
# of the entire page. Outputting this information to the log greatly increases
# the size of the log file.
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(
    logging.WARNING)


def get_chrome_browser():
    # LOCAL
    # options = webdriver.ChromeOptions()
    # Unable to hide "Chrome is being controlled by automated software" infobar
    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # Open Chrome for full size of screen
    # options.add_argument("--start-maximized")
    #  Will launch browser without UI(headless)
    # options.add_argument("--headless")

    # Below disabled options in local version
    # chrome_options.add_argument('--incognito')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--disable-extensions') #  ?

    # инициализируем драйвер с нужными опциями
    # CHROME_PATH = 'd:\\Python\\chromedriver_win32\\chromedriver.exe'
    # service = Service(CHROME_PATH)
    # browser = webdriver.Chrome(service=service, options=options)
    # LOCAL

    # VPS
    options = webdriver.ChromeOptions()
    # options.headless = headless_mode
    # options.add_argument("--disable-dev-shm-usage")
    #  Will launch browser without UI(headless)
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    # Add fake user agent
    current_user_agent = user_agent.chrome
    options.add_argument(f"--user-agent={current_user_agent}")
    # options.add_argument(
    #     f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    # logger.debug(f'current_user_agent: {current_user_agent}')

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    logger.debug(f'path_chromedriver: {path_chromedriver}')
    service = Service(path_chromedriver)
    # browser = webdriver.Chrome(service=service, options=options)
    browser = uc.Chrome()
    # Selenium Stealth settings
    # stealth(browser,
    #         languages=["en-US", "en"],
    #         user_agent=current_user_agent,
    #         vendor="Google Inc.",
    #         platform="Win32",
    #         webgl_vendor="Intel Inc.",
    #         renderer="Intel Iris OpenGL Engine",
    #         fix_hairline=True,
    #         )
    # VPS
    return browser


def get_firefox_browser():
    options = Options()
    #  Will launch browser without UI(headless)
    # options.headless = headless_mode
    # Disable logging
    # options.log.level = 'error'
    # options.add_argument("disable-logging")

    # Add fake user agent
    # current_user_agent = user_agent.firefox
    current_user_agent = user_agent.random
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", current_user_agent)

    logger.debug(f'path_geckodriver: {path_geckodriver}')
    service = FirefoxService(path_geckodriver)
    browser = webdriver.Firefox(firefox_profile=profile, service=service, options=options)
    return browser


def connect_to_page(browser, URL, page_number=1):
    if page_number == 1:
        page_url = URL
    else:
        page_url = f'{URL}?p={page_number}'
    browser.get(page_url)
    current_url = browser.current_url
    logger.debug(f'Current URL in connect_to_page: {current_url}')
    return current_url


def convert_date(date):
    if 'сек' in date:
        date_list = date.split()
        sec_str = date_list[0]
        if sec_str.isdigit():
            sec = int(date_list[0])
            converted_date = datetime.now() - timedelta(seconds=sec)
        else:
            converted_date = None
    elif 'мин' in date:
        date_list = date.split()
        minutes_str = date_list[0]
        if minutes_str.isdigit():
            minutes = int(date_list[0])
            converted_date = datetime.now() - timedelta(minutes=minutes)
        else:
            converted_date = None
    elif 'час' in date:
        date_list = date.split()
        hours_str = date_list[0]
        if hours_str.isdigit():
            hours = int(date_list[0])
            converted_date = datetime.now() - timedelta(hours=hours)
        else:
            converted_date = None
    elif 'день' or 'дня' or 'дней' in date:
        date_list = date.split()
        days_str = date_list[0]
        if days_str.isdigit():
            days = int(days_str)
            converted_date = datetime.now() - timedelta(days=days)
        else:
            converted_date = None
    elif 'недел' in date:
        date_list = date.split()
        weeks_str = date_list[0]
        if weeks_str.isdigit():
            weeks = int(date_list[0])
            converted_date = datetime.now() - timedelta(weeks=weeks)
        else:
            converted_date = None
    elif 'мес' in date:
        date_list = date.split()
        month_str = date_list[0]
        if month_str.isdigit():
            month = int(date_list[0])
            converted_date = datetime.now() - timedelta(days=30 * month)
        else:
            converted_date = None
    else:
        converted_date = None
    return converted_date

NONE_CRIMEA = (
    '/ahtanizovskaya/',
    '/anapa/',
    '/anapskaya/',
    '/dzhiginka/',
    '/golubitskaya/',
    '/krasnodarskiy_kray_strelka/',
    '/myshako/',
    '/novorossiysk/',
    '/sennoy/',
    '/starotitarovskaya/',
    '/supseh/',
    '/taman/',
    '/temryuk/',
    '/tsibanobalka/',
    '/vinogradnyy/',
    '/vityazevo/',
    '/vyshesteblievskaya/',
    '/yurovka/'
)
def remove_none_crimea(url):
    for item in NONE_CRIMEA:
        if item in url:
            return True
    return False

def parse_html_kvartiry_vtorichka(html, page):
    global vtorichka_counter
    logger.info(f'Hi from parse_html_kvartiry_vtorichka func!')
    BASE = 'https://www.avito.ru'
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('div[data-marker="item"]')
    logger.debug(
        '##################################################################')
    logger.debug(f'Number of items founded on page {page}:  {len(items)}')
    logger.debug(
        '##################################################################')
    data = {}
    # Get items_ids which are in database already
    item_ids_from_db = database.get_item_ids('kvartiry_vtorichka')
    logger.debug(
        f'Number of item_ids are already exist in database: {len(item_ids_from_db)}')
    for item in items:
        # We intercept the error in case some fields are not filled while
        # parsing. An error during parsing causes the whole process to stop.
        # In case of an error, we move on to parsing the next item.
        try:
            item_id = item['id']
            logger.debug(f'Detected item_id:  {item_id}')
            if item_id in item_ids_from_db:
                logger.debug(
                    f'Detected item_id is already exist in database: {item_id} | Skipped...')
                logger.debug(
                    '##############################################################')
                continue

            item_a = item.select_one('a[data-marker="item-title"]')
            logger.debug(f'item_a before remove_none_crimea:  {item_a}')
            if remove_none_crimea(item_a['href']):
                continue

            vtorichka_counter += 1
            logger.debug(
                f'vtorichka_counter: {vtorichka_counter}')
            logger.debug(
                f'Detected item_id is taken in work: {item_id}')
            logger.debug(
                '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            data_item_id = int(item['data-item-id'])
            logger.debug(f'data_item_id:  {data_item_id}')

            logger.debug(f'item_a:  {item_a}')
            item_url = BASE + item_a['href']
            logger.debug(f'item_url:  {item_url}')
            item_title = item_a.find('h3').text
            # Intercepting and processing errors in the title
            # of the announcement. Check is the title exist or not. There was
            # a case where the title field was not filled in for some reason,
            # and it caused a parsing error.
            if item_title:
                logger.debug(f'item_title:  {item_title}')
                item_title_list = item_title.split(',')
                logger.debug(f'item_title_list:  {item_title_list}')
                # item_number_of_rooms_list = None
                item_number_of_rooms = None
                item_type = None
                if '-к.' in item_title_list[0]:
                    item_number_of_rooms_list = item_title_list[0].split()
                    logger.debug(
                        f'item_number_of_rooms_list: {item_number_of_rooms_list}')
                    item_number_of_rooms_list_len = len(
                        item_number_of_rooms_list)
                    # If the number of rooms is not specified (Апартаменты,
                    # Апартаменты-студия, Квартира-студия, Апартаменты-студия,
                    # Своб. планировка
                    if item_number_of_rooms_list_len == 1:
                        item_number_of_rooms = None
                        item_type = item_number_of_rooms_list[0].lower()
                    # Стандартный вариант в большинстве случаев
                    elif item_number_of_rooms_list_len == 2:
                        item_number_of_rooms = int(
                            item_number_of_rooms_list[0].replace('-к.',
                                                                 ''))
                        item_type = item_number_of_rooms_list[1]
                    # There was a variant when the number of rooms was preceded
                    # by the word: Аукцион:
                    elif item_number_of_rooms_list_len == 3:
                        item_number_of_rooms = int(
                            item_number_of_rooms_list[1].replace('-к.',
                                                                 ''))
                        item_type = item_number_of_rooms_list[2]
                else:
                    item_number_of_rooms = None
                    item_type = item_title_list[0].lower()
                logger.debug(
                    f'item_number_of_rooms:  {item_number_of_rooms}')
                logger.debug(f'item_type:  {item_type}')

                # Getting an apartment area
                if len(item_title_list) > 3:
                    item_area = float(
                        (item_title_list[1] + '.' + item_title_list[
                            2]).replace(
                            '\xa0м²',
                            ''))
                else:
                    item_area = int(
                        item_title_list[1].replace('\xa0м\xb2', ''))
                logger.debug(f'item_area:  {item_area}')

                # Getting the floor on which the apartment is located and the
                # number of floors of the building
                item_floor_house = item_title_list[-1].replace('\xa0эт.',
                                                               '').strip()
                logger.debug(f'item_floor_house:  {item_floor_house}')
                item_floor_house_list = item_floor_house.split('/')
                logger.debug(
                    f'item_floor_house_list: {item_floor_house_list}')
                item_floor = int(item_floor_house_list[0].replace(' ', ''))
                logger.debug(f'item_floor:  {item_floor}')
                item_floors_in_house = int(
                    item_floor_house_list[1].replace(' ', ''))
                logger.debug(
                    f'item_floors_in_house:  {item_floors_in_house}')
            else:
                item_title = None
                item_type = None
                item_number_of_rooms = None
                item_area = None
                item_floor_house = None
                item_floor = None
                item_floors_in_house = None

            # Getting an item price.
            item_price_str = item.select_one('meta[itemprop="price"]') # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_price_str:  {item_price_str}')

            item_price = item_price_str.get('content') if item_price_str else None # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_price:  {item_price}')

            # Getting an item price currency.
            item_currency = item.select_one('meta[itemprop="priceCurrency"]').get('content') # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_currency:  {item_currency}')

            # Getting an item address. 08-06-2023 Исправлено после смены форматирования
            # Получение адреса.
            item_address_element = item.select(
                'div[data-marker="item-address"] p > span')
            item_address = item_address_element[0].text.strip() if item_address_element else None
            logger.debug(f'item_address: {item_address}')

            # Получение города (если присутствует).
            item_city_element = item_address_element[1]
            item_city = item_city_element.text.strip() if item_city_element else None
            logger.debug(f'item_city: {item_city}')

            # Getting an item publishing date.
            item_date_data = item.select_one('p[data-marker="item-date"]').text  # 24-05-2023 Исправление после смены форматирования
            # Convert '2 дня назад' or '5 минут назад' in normal calendar date.
            item_date = convert_date(item_date_data)
            logger.debug(
                f'item_date:  {item_date.strftime("%Y-%m-%d %H:%M")}')
            item_add_date = datetime.now()
        except Exception as err:
            logging.exception('Exception occurred during parsing!')
            continue
        # data writing into a dictionary.
        item_dict = {'data_item_id': data_item_id,
                     'item_id': item_id,
                     'item_url': item_url,
                     'item_title': item_title,
                     'item_type': item_type,
                     'item_number_of_rooms': item_number_of_rooms,
                     'item_area': item_area,
                     'item_floor_house': item_floor_house,
                     'item_floor': item_floor,
                     'item_floors_in_house': item_floors_in_house,
                     'item_price': item_price,
                     'item_currency': item_currency,
                     'item_address': item_address,
                     'item_city': item_city,
                     'property_type': 'квартиры-вторичка',
                     'item_date': item_date,
                     'item_add_date': item_add_date
                     }
        # Put data dictionary as 'value' in new dictionary
        # with item_id as 'key'.
        data[item_id] = item_dict
        logger.debug(
            '##############################################################')
    logger.debug(f'New items detected during parse: {len(data)}')
    logger.debug(
        '##############################################################')
    return data


def parse_html_kvartiry_novostroyka(html, page):
    global novostroy_counter
    BASE = 'https://www.avito.ru'
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('div[data-marker="item"]')
    logger.debug(
        '##################################################################')
    logger.debug(f'Number of items founded on page {page}:  {len(items)}')
    logger.debug(
        '##################################################################')
    data = {}
    # Get items_ids which are in database already
    item_ids_from_db = database.get_item_ids('kvartiry_novostroyka')
    logger.debug(
        f'Number of item_ids are already exist in database: {len(item_ids_from_db)}')
    for item in items:
        # We intercept the error in case some fields are not filled while
        # parsing. An error during parsing causes the whole process to stop.
        # In case of an error, we move on to parsing the next item.
        try:
            item_id = item['id']
            logger.debug(f'Detected item_id:  {item_id}')
            if item_id in item_ids_from_db:
                logger.debug(
                    f'Detected item_id is already exist in database: {item_id} | Skipped...')
                logger.debug(
                    '##############################################################')
                continue

            item_a = item.select_one('a[data-marker="item-title"]')
            logger.debug(f'item_a before remove_none_crimea:  {item_a}')
            if remove_none_crimea(item_a['href']):
                continue

            novostroy_counter += 1
            logger.debug(
                f'novostroy_counter: {novostroy_counter}')
            logger.debug(
                f'Detected item_id is taken in work: {item_id}')
            logger.debug(
                '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            data_item_id = int(item['data-item-id'])
            logger.debug(f'data_item_id:  {data_item_id}')

            logger.debug(f'item_a:  {item_a}')
            item_url = BASE + item_a['href']
            logger.debug(f'item_url:  {item_url}')
            item_title = item_a.find('h3').text
            # Intercepting and processing errors in the title
            # of the announcement. Check is the title exist or not. There was
            # a case where the title field was not filled in for some reason,
            # and it caused a parsing error.
            if item_title:
                logger.debug(f'item_title:  {item_title}')
                item_title_list = item_title.split(',')
                logger.debug(f'item_title_list:  {item_title_list}')
                # item_number_of_rooms_list = None
                item_number_of_rooms = None
                item_type = None
                if '-к.' in item_title_list[0]:
                    item_number_of_rooms_list = item_title_list[0].split()
                    logger.debug(
                        f'item_number_of_rooms_list: {item_number_of_rooms_list}')
                    item_number_of_rooms_list_len = len(
                        item_number_of_rooms_list)
                    # If the number of rooms is not specified (Апартаменты,
                    # Апартаменты-студия, Квартира-студия, Апартаменты-студия,
                    # Своб. планировка
                    if item_number_of_rooms_list_len == 1:
                        item_number_of_rooms = None
                        item_type = item_number_of_rooms_list[0].lower()
                    # Стандартный вариант в большинстве случаев
                    elif item_number_of_rooms_list_len == 2:
                        item_number_of_rooms = int(
                            item_number_of_rooms_list[0].replace('-к.',
                                                                 ''))
                        item_type = item_number_of_rooms_list[1]
                    # There was a variant when the number of rooms was preceded
                    # by the word: Аукцион:
                    elif item_number_of_rooms_list_len == 3:
                        item_number_of_rooms = int(
                            item_number_of_rooms_list[1].replace('-к.',
                                                                 ''))
                        item_type = item_number_of_rooms_list[2]
                else:
                    item_number_of_rooms = None
                    item_type = item_title_list[0].lower()
                logger.debug(
                    f'item_number_of_rooms:  {item_number_of_rooms}')
                logger.debug(f'item_type:  {item_type}')

                # Getting an apartment area
                if len(item_title_list) > 3:
                    item_area = float(
                        (item_title_list[1] + '.' + item_title_list[
                            2]).replace(
                            '\xa0м²',
                            ''))
                else:
                    item_area = int(
                        item_title_list[1].replace('\xa0м\xb2', ''))
                logger.debug(f'item_area:  {item_area}')

                # Getting the floor on which the apartment is located and the
                # number of floors of the building
                item_floor_house = item_title_list[-1].replace('\xa0эт.',
                                                               '').strip()
                logger.debug(f'item_floor_house:  {item_floor_house}')
                item_floor_house_list = item_floor_house.split('/')
                logger.debug(
                    f'item_floor_house_list: {item_floor_house_list}')
                item_floor = int(item_floor_house_list[0].replace(' ', ''))
                logger.debug(f'item_floor:  {item_floor}')
                item_floors_in_house = int(
                    item_floor_house_list[1].replace(' ', ''))
                logger.debug(
                    f'item_floors_in_house:  {item_floors_in_house}')
            else:
                item_title = None
                item_type = None
                item_number_of_rooms = None
                item_area = None
                item_floor_house = None
                item_floor = None
                item_floors_in_house = None

            # Getting an item price.
            item_price_str = item.select_one(
                'meta[itemprop="price"]')  # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_price_str:  {item_price_str}')

            item_price = item_price_str.get(
                'content') if item_price_str else None  # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_price:  {item_price}')

            # Getting an item price currency.
            item_currency = item.select_one(
                'meta[itemprop="priceCurrency"]').get(
                'content')  # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_currency:  {item_currency}')

            # Getting an item development name. 03-06-2023 Исправлено после смены форматирования
            item_development_name_element = item.select_one(
                'div[data-marker="item-address"] [data-marker="item-development-name"]')
            item_development_name = item_development_name_element.text.strip() if item_development_name_element else None
            logger.debug(f'item_development_name: {item_development_name}')

            # Getting an item address. 08-06-2023 Исправлено после смены форматирования
            # Получение адреса.
            item_address_element = item.select(
                'div[data-marker="item-address"] p > span')
            item_address = item_address_element[0].text.strip() if item_address_element else None
            logger.debug(f'item_address: {item_address}')

            # Получение города (если присутствует).
            item_city_element = item_address_element[1]
            item_city = item_city_element.text.strip() if item_city_element else None
            logger.debug(f'item_city: {item_city}')
            """
            item_address_element = item.select_one(
                'div[data-marker="item-address"] p > span')
            item_address = item_address_element.text.strip() if item_address_element else None
            logger.debug(f'item_address: {item_address}')

            item_city = None
            # Получение первого элемента <p>, содержащего два элемента <span>.
            item_p_element = item.select_one(
                'div[data-marker="item-address"] p:has(span + span)')

            if item_p_element:
                # Получение города.
                item_city_element = item_p_element.select_one(
                    'span:last-child')
                if item_city_element:
                    item_city = item_city_element.text.strip()
            logger.debug(f'item_city: {item_city}')
            """
            # Getting an item publishing date.
            item_date_data = item.select_one(
                'p[data-marker="item-date"]').text  # 24-05-2023 Исправление после смены форматирования
            # Convert '2 дня назад' or '5 минут назад' in normal calendar date.
            item_date = convert_date(item_date_data)
            logger.debug(
                f'item_date:  {item_date.strftime("%Y-%m-%d %H:%M")}')
            item_add_date = datetime.now()
        except Exception as err:
            logging.exception('Exception occurred during parsing!')
            continue
        # data writing into a dictionary.
        item_dict = {'data_item_id': data_item_id,
                     'item_id': item_id,
                     'item_url': item_url,
                     'item_title': item_title,
                     'item_type': item_type,
                     'item_number_of_rooms': item_number_of_rooms,
                     'item_area': item_area,
                     'item_floor_house': item_floor_house,
                     'item_floor': item_floor,
                     'item_floors_in_house': item_floors_in_house,
                     'item_price': item_price,
                     'item_currency': item_currency,
                     'item_development_name': item_development_name,
                     'item_address': item_address,
                     'item_city': item_city,
                     'property_type': 'квартиры-новострой',
                     'item_date': item_date,
                     'item_add_date': item_add_date
                     }
        # Put data dictionary as 'value' in new dictionary
        # with item_id as 'key'.
        data[item_id] = item_dict
        logger.debug(
            '##############################################################')
    logger.debug(f'New items detected during parse: {len(data)}')
    logger.debug(
        '##############################################################')
    return data


def parse_html_doma_dachi_kottedzhi(html, page):
    global doma_dachi_kottedzhi_counter
    BASE = 'https://www.avito.ru'
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('div[data-marker="item"]')
    logger.debug(
        '##################################################################')
    logger.debug(f'Number of items founded on page {page}:  {len(items)}')
    logger.debug(
        '##################################################################')
    data = {}
    # Get items_ids which are in database already
    item_ids_from_db = database.get_item_ids('doma_dachi_kottedzhi')
    logger.debug(
        f'Number of item_ids are already exist in database: {len(item_ids_from_db)}')
    for item in items:
        # We intercept the error in case some fields are not filled while
        # parsing. An error during parsing causes the whole process to stop.
        # In case of an error, we move on to parsing the next item.
        try:
            item_id = item['id']
            logger.debug(f'Detected item_id:  {item_id}')
            if item_id in item_ids_from_db:
                logger.debug(
                    f'Detected item_id is already exist in database: {item_id} | Skipped...')
                logger.debug(
                    '##############################################################')
                continue

            item_a = item.select_one('a[data-marker="item-title"]')
            logger.debug(f'item_a before remove_none_crimea:  {item_a}')
            if remove_none_crimea(item_a['href']):
                continue

            doma_dachi_kottedzhi_counter += 1
            logger.debug(
                f'doma_dachi_kottedzhi_counter: {doma_dachi_kottedzhi_counter}')
            logger.debug(
                f'Detected item_id is taken in work: {item_id}')
            logger.debug(
                '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            data_item_id = int(item['data-item-id'])
            logger.debug(f'data_item_id:  {data_item_id}')

            logger.debug(f'item_a:  {item_a}')
            item_url = BASE + item_a['href']
            logger.debug(f'item_url:  {item_url}')
            item_title = item_a.find('h3').text
            # Intercepting and processing errors in the title
            # of the announcement. Check is the title exist or not. There was
            # a case where the title field was not filled in for some reason,
            # and it caused a parsing error.
            if item_title:
                logger.debug(f'item_title:  {item_title}')
                if '\xa0' in item_title:
                    item_title = item_title.replace('\xa0', ' ')
                item_title_list = item_title.split(' ')
                logger.debug(f'item_title_list:  {item_title_list}')
                item_type = None
                item_land_area = None
                item_area = None
                if item_title_list[0]:
                    item_type = item_title_list[0].lower()
                    logger.debug(
                        f'item_type: {item_type}')
                # Getting a house area
                if item_title_list[1]:
                    if ',' in item_title_list[1]:
                        item_area = float(
                            item_title_list[1].replace(',', '.'))
                    else:
                        item_area = int(item_title_list[1])
                logger.debug(f'item_area:  {item_area}')
                if item_title_list[5]:
                    if ',' in item_title_list[5]:
                        item_land_area = float(
                            item_title_list[5].replace(',', '.'))
                    else:
                        item_land_area = int(item_title_list[5])
            else:
                item_title = None
                item_type = None
                item_area = None
                item_land_area = None

            # Getting an item price.
            # item_price_str = item.select_one(
            #     'span[class*="price-text-"]').text
            item_price_str = item.select_one(
                'meta[itemprop="price"]')  # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_price_str:  {item_price_str}')
            # item_price = int(
            #     ''.join(
            #         char for char in item_price_str if char.isdecimal()))
            item_price = item_price_str.get(
                'content') if item_price_str else None  # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_price:  {item_price}')

            # Getting an item price currency.
            # item_currency = item.select_one(
            #     'span[class*="price-currency-"]').text
            item_currency = item.select_one(
                'meta[itemprop="priceCurrency"]').get(
                'content')  # 24-05-2023 Исправление после смены форматирования
            logger.debug(f'item_currency:  {item_currency}')

            # Getting an item city.  03-06-2023 Исправлено после смены форматирования
            item_city = None
            item_address = None
            
            item_city_element = item.select_one(
                'div[data-marker="item-address"] p > span')
            logger.debug(f'item_city_element: {item_city_element}')
            if item_city_element:
                item_city = item_city_element.text.strip()

            logger.debug(f'item_city: {item_city}')

            # Getting an item publishing date.
            item_date_data = item.select_one(
                'p[data-marker="item-date"]').text  # 24-05-2023 Исправление после смены форматирования
            # Convert '2 дня назад' or '5 минут назад' in normal calendar date.
            item_date = convert_date(item_date_data)
            logger.debug(
                f'item_date:  {item_date.strftime("%Y-%m-%d %H:%M")}')
            item_add_date = datetime.now()
        except Exception as err:
            logging.exception('Exception occurred during parsing!')
            continue
        # data writing into a dictionary.
        item_dict = {'data_item_id': data_item_id,
                     'item_id': item_id,
                     'item_url': item_url,
                     'item_title': item_title,
                     'item_type': item_type,
                     'item_area': item_area,
                     'item_land_area': item_land_area,
                     'item_price': item_price,
                     'item_currency': item_currency,
                     'item_address': item_address,
                     'item_city': item_city,
                     'property_type': 'Дома, дачи и коттеджи',
                     'item_date': item_date,
                     'item_add_date': item_add_date
                     }
        # Put data dictionary as 'value' in new dictionary
        # with item_id as 'key'.
        data[item_id] = item_dict
        logger.debug(
            '##############################################################')
    logger.debug(f'New items detected during parse: {len(data)}')
    logger.debug(
        '##############################################################')
    return data
