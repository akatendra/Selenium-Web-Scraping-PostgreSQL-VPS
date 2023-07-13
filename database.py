import psycopg2
from psycopg2 import Error
import logging.config
import scraper
from datetime import datetime
# from config_local import user, password, host, port, database
from config_vps import user, password, host, port, database

# Set up logging
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def execute_sql_query(sql, fetch=True, data=None):
    try:
        # Connection to PostgreSQL DB
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        with connection:
            # Курсор для выполнения операций с базой данных
            with connection.cursor() as cursor:
                if cursor:
                    logger.info('PostgreSQL connected!')
                if data is None:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, data)
                if fetch is True:
                    return cursor.fetchall()
    except (Exception, Error) as error:
        logger.debug("Error during work with PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info("Connection with PostgreSQL closed!")


def create_table_kvartiry_vtorichka():
    sql_create_table_kvartiry_vtorichka = '''
                            CREATE TABLE IF NOT EXISTS kvartiry_vtorichka (
                            id SERIAL PRIMARY KEY, 
                            data_item_id BIGINT NOT NULL,
                            item_id VARCHAR(255) NOT NULL,
                            item_url VARCHAR(512) NOT NULL,
                            item_title VARCHAR(255),
                            item_type VARCHAR(255),
                            item_number_of_rooms INTEGER,
                            item_area REAL,
                            item_floor_house VARCHAR(255),
                            item_floor INTEGER,
                            item_floors_in_house INTEGER,
                            item_price INTEGER,
                            item_currency VARCHAR(255) NOT NULL,
                            item_address VARCHAR(512),
                            item_city VARCHAR(255),
                            property_type VARCHAR(255) NOT NULL,
                            item_date TIMESTAMP NOT NULL,
                            item_add_date TIMESTAMP NOT NULL 
                            );'''
    execute_sql_query(sql_create_table_kvartiry_vtorichka, fetch=False)
    logger.info('Table kvartiry_vtorichka created!')


def create_table_kvartiry_novostroyka():
    sql_create_table_kvartiry_novostroyka = '''
                            CREATE TABLE IF NOT EXISTS kvartiry_novostroyka (
                            id SERIAL PRIMARY KEY, 
                            data_item_id BIGINT NOT NULL,
                            item_id VARCHAR(255) NOT NULL,
                            item_url VARCHAR(512) NOT NULL,
                            item_title VARCHAR(255),
                            item_type VARCHAR(255),
                            item_number_of_rooms INTEGER,
                            item_area REAL,
                            item_floor_house VARCHAR(255),
                            item_floor INTEGER,
                            item_floors_in_house INTEGER,
                            item_price INTEGER,
                            item_currency VARCHAR(255) NOT NULL,
                            item_development_name VARCHAR(255),
                            item_address VARCHAR(255),
                            item_city VARCHAR(255),
                            property_type VARCHAR(255) NOT NULL,
                            item_date TIMESTAMP NOT NULL,
                            item_add_date TIMESTAMP NOT NULL
                            );'''
    execute_sql_query(sql_create_table_kvartiry_novostroyka, fetch=False)
    logger.info('Table kvartiry_novostroyka created!')


def create_table_doma_dachi_kottedzhi():
    sql_create_table_doma_dachi_kottedzhi = '''
                            CREATE TABLE IF NOT EXISTS doma_dachi_kottedzhi (
                            id SERIAL PRIMARY KEY, 
                            data_item_id BIGINT NOT NULL,
                            item_id VARCHAR(255) NOT NULL,
                            item_url VARCHAR(512),
                            item_title VARCHAR(255),
                            item_type VARCHAR(255),
                            item_area REAL,
                            item_land_area REAL,
                            item_price INTEGER,
                            item_currency VARCHAR(255) NOT NULL,
                            item_address VARCHAR(255),
                            item_city VARCHAR(255),
                            property_type VARCHAR(255) NOT NULL,
                            item_date TIMESTAMP NOT NULL,
                            item_add_date TIMESTAMP NOT NULL
                            );'''
    execute_sql_query(sql_create_table_doma_dachi_kottedzhi, fetch=False)
    logger.info('Table doma_dachi_kottedzhi created!')


def get_item_ids(table):
    sql_get_item_ids = f'SELECT item_id FROM {table};'
    item_ids = execute_sql_query(sql_get_item_ids)
    item_ids_tuple = set((item[0] for item in item_ids))
    logger.debug(f'Items_ids tuple received: {len(item_ids_tuple)}')
    return item_ids_tuple


def get_item_ids_list(table):
    sql_get_item_ids = f'SELECT item_id FROM {table};'
    item_ids = execute_sql_query(sql_get_item_ids)
    item_ids = list((item[0] for item in item_ids))
    logger.debug(f'Items_ids list received: {len(item_ids)}')
    return item_ids


def get_days_count(table):
    sql_get_days_count = f'''
                            SELECT Count(*)
                            FROM   (SELECT To_char(item_date, 'YYYY-MM-DD')
                                    FROM   {table}
                                    GROUP  BY To_char(item_date, 'YYYY-MM-DD')) AS itmd;
                          '''
    days_count = execute_sql_query(sql_get_days_count)
    logger.debug(f'days_count: {days_count}')
    return days_count


def get_days_count_4_period(table, date_start, date_end):
    sql_get_days_count_4_period = f'''
                            SELECT Count(*)
                            FROM   (SELECT To_char(item_date, 'YYYY-MM-DD')
                                    FROM   {table}
                                    WHERE  item_date BETWEEN '{date_start}'::date AND '{date_end}'::date
                                    GROUP  BY To_char(item_date, 'YYYY-MM-DD')) AS itmd;
                          '''
    days_count_4_period = execute_sql_query(sql_get_days_count_4_period)
    logger.debug(f'days_count_4_period: {date_start}/{date_end} {days_count_4_period}')
    return days_count_4_period


def write_to_db_kvartiry_vtorichka(data):
    table = 'kvartiry_vtorichka'
    # values = ', '.join(['%s'] * 17)
    sql_put_data = f'''
                   INSERT INTO {table}
                   (data_item_id, 
                    item_id, 
                    item_url, 
                    item_title,
                    item_type, 
                    item_number_of_rooms, 
                    item_area, 
                    item_floor_house, 
                    item_floor, 
                    item_floors_in_house, 
                    item_price, 
                    item_currency, 
                    item_address, 
                    item_city,
                    property_type,
                    item_date, 
                    item_add_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                   '''
    item_ids = set(data.keys())
    logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_database = get_item_ids(table)
    item_ids_to_write = item_ids.difference(item_ids_database)
    logger.debug(f'item_ids_to_write: {item_ids_to_write}')
    logger.debug(f'vtorichka_counter: {scraper.vtorichka_counter}')
    for item_id in item_ids_to_write:
        # for item_id in item_ids:
        logger.debug(f'item_id: {item_id}')
        # Check if item_id is already exist in database
        # if item_id not in item_ids_database:
        data_tuple = tuple(
            (item_data for item_data in data[item_id].values()))
        logger.debug(f'{type(data_tuple)}, {data_tuple}')
        execute_sql_query(sql_put_data, fetch=False, data=data_tuple)
    logger.info('Data saved into table kvartiry_vtorichka!')


def write_to_db_kvartiry_novostroyka(data):
    table = 'kvartiry_novostroyka'
    # values = ', '.join(['%s'] * 18)
    sql_put_data = f'''
                   INSERT INTO {table}
                   (data_item_id, 
                    item_id, 
                    item_url, 
                    item_title,
                    item_type, 
                    item_number_of_rooms, 
                    item_area, 
                    item_floor_house, 
                    item_floor, 
                    item_floors_in_house, 
                    item_price, 
                    item_currency,
                    item_development_name,
                    item_address, 
                    item_city,
                    property_type,
                    item_date, 
                    item_add_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                   '''
    item_ids = set(data.keys())
    # logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_database = get_item_ids(table)
    item_ids_to_write = item_ids.difference(item_ids_database)
    for item_id in item_ids_to_write:
        # logger.debug(f'item_id: {item_id}')
        data_tuple = tuple((item_data for item_data in data[item_id].values()))
        # logger.debug(f'{type(data_tuple)}, {data_tuple}')
        execute_sql_query(sql_put_data, fetch=False, data=data_tuple)
    logger.info('Data saved into table kvartiry_novostroyka!')


def write_to_db_doma_dachi_kottedzhi(data):
    table = 'doma_dachi_kottedzhi'
    # values = ', '.join(['%s'] * 14)
    # sql_put_data = f'''
    #                INSERT INTO {table}
    #                (data_item_id,
    #                 item_id,
    #                 item_url,
    #                 item_title,
    #                 item_type,
    #                 item_area,
    #                 item_land_area,
    #                 item_price,
    #                 item_currency,
    #                 item_address,
    #                 item_city,
    #                 property_type,
    #                 item_date,
    #                 item_add_date)
    #                 VALUES ({values});
    #                '''
    sql_put_data = f'''
                       INSERT INTO {table}
                       (data_item_id, 
                        item_id, 
                        item_url, 
                        item_title,
                        item_type, 
                        item_area,
                        item_land_area, 
                        item_price, 
                        item_currency,
                        item_address, 
                        item_city,
                        property_type,
                        item_date, 
                        item_add_date) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                       '''
    item_ids = set(data.keys())
    # logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_database = get_item_ids(table)
    item_ids_to_write = item_ids.difference(item_ids_database)
    for item_id in item_ids_to_write:
        # logger.debug(f'item_id: {item_id}')
        data_tuple = tuple((item_data for item_data in data[item_id].values()))
        # logger.debug(f'{type(data_tuple)}, {data_tuple}')
        execute_sql_query(sql_put_data, fetch=False, data=data_tuple)
    logger.info('Data saved into table doma_dachi_kottedzhi!')


def duplicates_check(table):
    item_ids = get_item_ids(table)
    logger.debug(f'{type(item_ids)}, {len(item_ids)}, {item_ids}')
    item_ids_list = get_item_ids_list(table)
    logger.debug(
        f'{type(item_ids_list)}, {len(item_ids_list)}, {item_ids_list}')


###############################################################################
######################## VISUALISATION QUERIES ################################
###############################################################################
def get_item_count_per_day(table):
    sql_get_item_count_per_day = f'''
                                 SELECT 
                                     to_char(item_date, 'YYYY-MM-DD Dy'), 
                                     COUNT(*) 
                                 FROM 
                                    {table} 
                                 GROUP BY 
                                    to_char(item_date, 'YYYY-MM-DD Dy');
                                 '''
    item_count_per_day = execute_sql_query(sql_get_item_count_per_day)
    # logger.debug(
    #     f'item_count_per_day received: {len(item_count_per_day)} | {item_count_per_day}')
    return item_count_per_day


def get_item_count_per_day2(table):
    sql_get_item_count_per_day = f'''
                                 SELECT 
                                     to_char(item_date, 'YYYY-MM-DD Dy') 
                                 FROM 
                                    {table};
                                 '''
    item_count_per_day = execute_sql_query(sql_get_item_count_per_day)
    # logger.debug(
    #     f'item_count_per_day received: {len(item_count_per_day)} | {item_count_per_day}')
    return item_count_per_day

def get_item_count_per_day2_4_period(table, date_start, date_end):
    sql_get_item_count_per_day_4_period = f'''
                                 SELECT 
                                     to_char(item_date, 'YYYY-MM-DD Dy') 
                                 FROM 
                                    {table}
                                 WHERE
                                    item_date BETWEEN '{date_start}'::date AND '{date_end}'::date;
                                 '''
    item_count_per_day_4_period = execute_sql_query(sql_get_item_count_per_day_4_period)
    logger.debug(
        f'item_count_per_day_4_period received: {len(item_count_per_day_4_period)} | {item_count_per_day_4_period}')
    return item_count_per_day_4_period


def get_item_count_per_day3():
    sql_get_item_count_per_day = f'''
                                    SELECT to_char(item_date, 'YYYY-MM-DD Dy'),
                                    property_type
                                    FROM kvartiry_vtorichka
                                    UNION ALL
                                    SELECT to_char(item_date, 'YYYY-MM-DD Dy'),
                                    property_type
                                    FROM kvartiry_novostroyka
                                    UNION ALL
                                    SELECT to_char(item_date, 'YYYY-MM-DD Dy'),
                                    property_type
                                    FROM doma_dachi_kottedzhi
                                 '''
    item_count_per_day = execute_sql_query(sql_get_item_count_per_day)
    # logger.debug(
    #     f'item_count_per_day received: {len(item_count_per_day)} | {item_count_per_day}')
    return item_count_per_day


def get_item_date_price_area(table):
    sql_get_item_date_price_area = f'''
                                 SELECT
                                     to_char(item_date, 'YYYY-MM-DD Dy'),
                                     item_price,
                                     item_area
                                 FROM 
                                    {table};
                                 '''
    item_date_price_area = execute_sql_query(sql_get_item_date_price_area)
    # logger.debug(
    #     f'item_date_price_area received: {len(item_date_price_area)} | {item_date_price_area}')
    return item_date_price_area


def get_item_date_price_area_average(table):
    sql_get_item_date_price_area_av = f'''
                                 SELECT
                                     to_char(item_date, 'YYYY-MM-DD Dy'),
                                    ROUND (AVG (item_price / item_area)) AS av_price_per_sq_m
                                 FROM 
                                    {table}
                                 GROUP BY 
                                    to_char(item_date, 'YYYY-MM-DD Dy');
                                 '''
    item_date_price_area_av = execute_sql_query(
        sql_get_item_date_price_area_av)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_date_price_area_av)} | {item_date_price_area_av}')
    return item_date_price_area_av


def get_item_date_price_area_average_union():
    sql_get_item_date_price_area_av_union = f'''
                                            SELECT to_char(item_date, 'YYYY-MM-DD Dy'),
                                                   ROUND (AVG (item_price / item_area)) AS av_price_per_sq_m,
                                                   property_type
                                            FROM kvartiry_vtorichka
                                            GROUP BY to_char(item_date, 'YYYY-MM-DD Dy'),
                                                     property_type
                                            UNION
                                            SELECT to_char(item_date, 'YYYY-MM-DD Dy'),
                                                   ROUND (AVG (item_price / item_area)) AS av_price_per_sq_m,
                                                   property_type
                                            FROM kvartiry_novostroyka
                                            GROUP BY to_char(item_date, 'YYYY-MM-DD Dy'),
                                                     property_type
                                            UNION
                                            SELECT to_char(item_date, 'YYYY-MM-DD Dy'),
                                                   ROUND (AVG (item_price / item_area)) AS av_price_per_sq_m,
                                                   property_type
                                            FROM doma_dachi_kottedzhi
                                            GROUP BY to_char(item_date, 'YYYY-MM-DD Dy'),
                                                   property_type
                                            ;
                                            '''
    item_date_price_area_av_union = execute_sql_query(
        sql_get_item_date_price_area_av_union)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_date_price_area_av_union)} | {item_date_price_area_av_union}')
    return item_date_price_area_av_union


def get_item_date_price_area_average_union_4_period(date_start, date_end):
    sql_get_item_date_price_area_average_union_4_period = f'''
        SELECT to_char(item_date::date, 'YYYY-MM-DD Dy'),
               ROUND(AVG(item_price / item_area)) AS av_price_per_sq_m,
               property_type
        FROM kvartiry_vtorichka
        WHERE item_date BETWEEN '{date_start}'::date AND '{date_end}'::date
        GROUP BY to_char(item_date::date, 'YYYY-MM-DD Dy'),
                 property_type
        UNION
        SELECT to_char(item_date::date, 'YYYY-MM-DD Dy'),
               ROUND(AVG(item_price / item_area)) AS av_price_per_sq_m,
               property_type
        FROM kvartiry_novostroyka
        WHERE item_date BETWEEN '{date_start}'::date AND '{date_end}'::date
        GROUP BY to_char(item_date::date, 'YYYY-MM-DD Dy'),
                 property_type
        UNION
        SELECT to_char(item_date::date, 'YYYY-MM-DD Dy'),
               ROUND(AVG(item_price / item_area)) AS av_price_per_sq_m,
               property_type
        FROM doma_dachi_kottedzhi
        WHERE item_date BETWEEN '{date_start}'::date AND '{date_end}'::date
        GROUP BY to_char(item_date::date, 'YYYY-MM-DD Dy'),
                 property_type
                                            ;
                                            '''
    item_date_price_area_av_union_4_period = execute_sql_query(sql_get_item_date_price_area_average_union_4_period)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_date_price_area_av_union)} | {item_date_price_area_av_union}')
    return item_date_price_area_av_union_4_period

def get_item_count_by_cities(table):
    sql_get_item_count_by_cities = f'''
                                 SELECT
                                     item_city
                                 FROM 
                                    {table};
                                 '''
    item_count_by_cities = execute_sql_query(sql_get_item_count_by_cities)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_count_by_cities)} | {item_count_by_cities}')
    return item_count_by_cities


def get_top10_cities(table):
    sql_get_order_vector = f'''
                            SELECT item_city
                            FROM
                              (SELECT item_city,
                                      COUNT(*) AS item_count
                               FROM {table}
                               GROUP BY item_city
                               ORDER BY item_count DESC
                               LIMIT 10) AS top10cities
                               ;
                            '''
    order_vector = execute_sql_query(sql_get_order_vector)
    order_vector = list((item[0] for item in order_vector))
    # logger.debug(
    #     f'item_date_price_area_av received: {len(order_vector)} | {order_vector}')
    sql_get_top10_cities = f'''
                            SELECT item_city
                            FROM {table}
                            WHERE item_city IN
                                (SELECT item_city
                                 FROM
                                   (SELECT item_city,
                                           COUNT(*)
                                    FROM {table}
                                    GROUP BY item_city
                                    ORDER BY COUNT(*) DESC
                                    LIMIT 10) AS top10cities)
                                    ;
                                 '''
    top10_cities = execute_sql_query(sql_get_top10_cities)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(top10_cities)} | {top10_cities}')
    return order_vector, top10_cities


def get_item_count_sevastopol(table):
    sql_get_item_count_sevastopol = f'''
                                 SELECT
                                     to_char(item_date, 'YYYY-MM-DD Dy'),
                                     COUNT(*)
                                 FROM 
                                    {table}
                                 WHERE
                                     item_city = 'Севастополь'
                                 GROUP BY 
                                    to_char(item_date, 'YYYY-MM-DD Dy')
                                 ORDER BY
                                     to_char(item_date, 'YYYY-MM-DD Dy')
                                 '''
    item_count_sevastopol = execute_sql_query(sql_get_item_count_sevastopol)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_count_sevastopol)} | {item_count_sevastopol}')
    return item_count_sevastopol


def get_item_count_sevastopol_simple(table):
    sql_get_item_count_sevastopol = f'''
                                 SELECT
                                     to_char(item_date, 'YYYY-MM-DD Dy')
                                 FROM 
                                    {table}
                                 WHERE
                                     item_city LIKE '%Севастополь%'
                                 ORDER BY
                                     to_char(item_date, 'YYYY-MM-DD Dy')
                                 '''
    item_count_sevastopol = execute_sql_query(sql_get_item_count_sevastopol)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_count_sevastopol)} | {item_count_sevastopol}')
    return item_count_sevastopol


def get_item_count_sevastopol_4_period(table, date_start, date_end):
    sql_get_item_count_sevastopol_4_period = f'''
                                 SELECT
                                     to_char(item_date, 'YYYY-MM-DD Dy')
                                 FROM 
                                    {table}
                                 WHERE
                                     item_city LIKE '%Севастополь%'
                                 AND
                                     item_date BETWEEN '{date_start}'::date AND '{date_end}'::date
                                 ORDER BY
                                     to_char(item_date, 'YYYY-MM-DD Dy')
                                 '''
    item_count_sevastopol_4_period = execute_sql_query(sql_get_item_count_sevastopol_4_period)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_count_sevastopol)} | {item_count_sevastopol}')
    return item_count_sevastopol_4_period

def get_item_cities():
    sql_get_item_cities = f'''
                            SELECT
                                item_city
                            FROM
                                kvartiry_vtorichka
                            GROUP BY
                                item_city
                            UNION
                            SELECT
                                item_city
                            FROM
                                kvartiry_novostroyka
                            GROUP BY 
                                item_city                                     
                                     '''
    item_cities = execute_sql_query(sql_get_item_cities)
    # logger.debug(
    #     f'item_date_price_area_av received: {len(item_cities)} | {item_cities}')
    return item_cities


# def rename_table_items():
#     sql_rename_table_items = '''
#                            ALTER TABLE items
#                            RENAME TO kvartiry_vtorichka;
#                            '''
#     execute_sql_query(sql_rename_table_items)


if __name__ == '__main__':
    create_table_kvartiry_vtorichka()
    create_table_kvartiry_novostroyka()
    create_table_doma_dachi_kottedzhi()
    # duplicates_check('kvartiry_vtorichka')
    # duplicates_check('kvartiry_novostroyka')
    # rename_table_items()
    # get_item_ids('kvartiry_vtorichka')
    # get_item_ids_list('kvartiry_vtorichka')
    # print(get_item_count_per_day('kvartiry_vtorichka'))
    # print(get_item_count_per_day2('kvartiry_vtorichka'))
    # print(get_item_count_per_day3())
    # print(get_item_date_price_area('kvartiry_vtorichka'))
    # print(get_item_date_price_area_average('kvartiry_vtorichka'))
    # print(get_item_date_price_area_average_union())
    # print(get_item_count_per_day('kvartiry_vtorichka'))
    # print(get_item_count_by_cities('kvartiry_vtorichka'))
    # print(get_top10_cities('kvartiry_vtorichka'))
    # print(get_item_count_sevastopol('kvartiry_vtorichka'))
    # print(get_item_count_sevastopol_simple('kvartiry_vtorichka'))
    # print(get_item_cities())
