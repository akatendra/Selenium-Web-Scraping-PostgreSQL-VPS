from datetime import timedelta, datetime
import time
import request

import scraper
import database
import visualisation
import telegram

import logging.config
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
    start_page = 1
    end_page = 100

    # kvartiry_vtorichka
    run_flow(url_kvartiry_vtorichka,
             start_page,
             end_page,
             parse_vtorichka,
             write_db_vtorichka
            )

    # kvartiry_novostroyka
    logger.info(f'Start parsing kvartiry_novostroyka')
    end_page = 47

    run_flow(url_kvartiry_novostroyka,
             start_page,
             end_page,
             parse_novostroyka,
             write_db_novostroyka
            )

    # doma_dachi_kottedzhi
    logger.info(f'Start parsing doma_dachi_kottedzhi')
    end_page = 100

    run_flow(url_doma_dachi_kottedzhi,
             start_page,
             end_page,
             parse_doma,
             write_db_doma
             )


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
