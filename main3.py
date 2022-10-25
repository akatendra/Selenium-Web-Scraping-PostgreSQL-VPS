from datetime import datetime
import time

import request
import scraper
import database
import visualisation
import telegram
import logging.config
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, wait
from random import randint


def spent_time():
    global start_time
    sec_all = time.time() - start_time
    if sec_all > 60:
        minutes = sec_all // 60
        sec = sec_all % 60
        time_str = f'| {int(minutes)} min {round(sec, 1)} sec'
    else:
        time_str = f'| {round(sec_all, 1)} sec'
    start_time = time.time()
    return time_str


def sleep_time(max_sec):
    rand_time = randint(1, max_sec)
    time.sleep(rand_time)
    return rand_time


def sleep_time_minutes(max_min):
    rand_time = randint(1, max_min)
    time.sleep(rand_time * 60)
    return rand_time


def run_flow(URL, start_page, end_page, parse_func, write_to_db_func):
    logger.info(f'Hi from run_flow func!')
    logger.debug(
        f'Browser for pages {URL} | {start_page}-{end_page} opened: {spent_time()}')
    # Wait random seconds
    sleep_time(5)
    current_page = start_page
    while current_page <= end_page:
        logger.debug(f'Take in work page: {current_page}')
        if current_page == 1:
            page_url = URL
        else:
            page_url = f'{URL}?p={current_page}'
        ####################################################################
        ####################  PAGE PROCESSING  #############################
        ####################################################################
        logger.debug(
            '##################################################################')
        logger.debug(f'Scraping page #{current_page}...')
        logger.debug(
            '##################################################################')
        html = request.get_request(page_url)
        logger.debug(
            f'Page_source of page {current_page} received: {spent_time()}')
        output_data = parse_func(html, current_page)
        logger.debug(
            f'Output_data of page {current_page} received: {spent_time()}')
        write_to_db_func(output_data)

        ####################################################################
        current_page += 1


def thread_pool(func, url, pages, parse_func, write_to_db_func):
    futures = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for page in pages:
            futures.append(
                executor.submit(func, url, page[0], page[1], parse_func,
                                write_to_db_func))
            # Wait random seconds
            sleep_time(10)
            logger.debug(
                f'ThreadPoolExecutor take in work pages: {url} | {page[0]}-{page[1]}')
    # Wait for ending of all running processes
    wait(futures)


if __name__ == "__main__":
    # Set up logging
    logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    # Remove matplotlib.font_manager from logging
    # logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
    # Remove all matplotlib from logging
    logging.getLogger('matplotlib').setLevel(logging.WARNING)

    # Set the variables values
    url_kvartiry_vtorichka = 'https://www.avito.ru/respublika_krym/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg'
    url_kvartiry_novostroyka = 'https://www.avito.ru/respublika_krym/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg'
    url_doma_dachi_kottedzhi = 'https://www.avito.ru/respublika_krym/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ'
    current_page = 1
    last_page = 100
    output_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    browsers = []
    # End of variables values setting

    # Import parse functions
    parse_vtorichka = scraper.parse_html_kvartiry_vtorichka
    parse_novostroyka = scraper.parse_html_kvartiry_novostroyka
    parse_doma = scraper.parse_html_doma_dachi_kottedzhi

    # Import writing to DB functions
    write_db_vtorichka = database.write_to_db_kvartiry_vtorichka
    write_db_novostroyka = database.write_to_db_kvartiry_novostroyka
    write_db_doma = database.write_to_db_doma_dachi_kottedzhi

    logger.info('Start...')

    # Delay running the program for a random number of minutes
    # to emulate human behavior.
    time_to_sleep = sleep_time_minutes(22)
    logger.debug(f'Sleep for {time_to_sleep} minutes.')

    time_begin = start_time = time.time()

    logger.info(f'Start parsing kvartiry_vtorichka')
    # Adding multithreading

    # kvartiry_vtorichka

    # 6 threads
    # pages = [(1, 14), (15, 32), (33, 48), (49, 63), (64, 82), (83, 100)]
    # 5 threads
    pages = [(1, 21), (22, 41), (42, 60), (61, 81), (82, 100)]
    # 4 threads
    # pages = [(1, 24), (25, 51), (52, 77), (78, 100)]
    # 1 thread
    # pages = [(1, 3)]

    # 8 threads
    # pages = [(1, 11), (12, 24), (25, 36), (37, 49), (50, 63), (64, 77), (78, 90), (91, 100)]

    thread_pool(run_flow,
                url_kvartiry_vtorichka,
                pages,
                parse_vtorichka,
                write_db_vtorichka
                )

    # kvartiry_novostroyka
    logger.info(f'Start parsing kvartiry_novostroyka')
    pages.clear()
    # 6 threads
    # pages = [(1, 9), (10, 17), (18, 23), (24, 32), (33, 41), (42, 47)]
    # 5 threads
    pages = [(1, 9), (10, 20), (21, 30), (31, 42), (42, 47)]
    # 4 threads
    # pages = [(1, 12), (13, 24), (25, 36), (37, 47)]
    # 1 thread
    # pages = [(1, 3)]

    # 8 threads
    # pages = [(1, 5), (6, 11), (12, 17), (18, 25), (26, 31), (32, 37), (38, 43), (44, 47)]

    thread_pool(run_flow,
                url_kvartiry_novostroyka,
                pages,
                parse_novostroyka,
                write_db_novostroyka
                )

    # doma_dachi_kottedzhi
    logger.info(f'Start parsing doma_dachi_kottedzhi')
    pages.clear()
    # 6 threads
    # pages = [(1, 14), (15, 32), (33, 48), (49, 63), (64, 82), (83, 100)]
    # 5 threads
    pages = [(1, 20), (21, 41), (42, 59), (60, 80), (81, 100)]
    # 4 threads
    # pages = [(1, 24), (25, 51), (52, 77), (78, 100)]
    # 1 thread
    # pages = [(1, 3)]

    # 8 threads
    # pages = [(1, 11), (12, 24), (25, 36), (37, 49), (50, 63), (64, 77), (78, 90), (91, 100)]

    thread_pool(run_flow,
                url_doma_dachi_kottedzhi,
                pages,
                parse_doma,
                write_db_doma
                )

    # Closing all unclosed browsers
    for browser in browsers:
        if browser.service.is_connectable():
            browser.quit()

    time_end = time.time()
    elapsed_time = time_end - time_begin
    if elapsed_time > 60:
        elapsed_minutes = elapsed_time // 60
        elapsed_sec = elapsed_time % 60
        elapsed_time_str = f'| {int(elapsed_minutes)} min {round(elapsed_sec, 1)} sec'
    else:
        elapsed_time_str = f'| {round(elapsed_time, 1)} sec'
    message = f'Elapsed run time: {elapsed_time_str} seconds | New vtorichka items: {scraper.vtorichka_counter} | New novostroy items: {scraper.novostroy_counter} | New doma_dachi_kottedzhi items: {scraper.doma_dachi_kottedzhi_counter}'
    logger.info(message)

    # Send report to telegram
    telegram.send_message(message)

    # Get visualization
    visualisation.get_visualization()
