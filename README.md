# Web Scraping with Selenium and save into PostgreSQL DB #
Web Scraping site for information on real estate sales and saving scraped info into PostgreSQL database. Learning project.
***
### The project is built on libraries: ###
Selenium

BeautifulSoup

psycopg2

request

seaborn

pandas

concurrent.futures

***
The project is deployed on a VPS:

https://realty.crimea.ua/

The file main2.py is used now.

It uses request library because it was easier than using Selenium. Since the site blocked parsing by IP I had to use proxy service scrapeops.io. The visualization of the site is based on aiohttp_jinja2. Code from this Git should be in scraper folder here:

https://github.com/akatendra/Silenium-Web-Scraping-PostgreSQL


The duration of parsing 3 categories of the site averaged 60-80 minutes.

***
main.py - the original version of the parser with Selenium. Gave up using it because of its unwieldiness. This code works on the local computer, but on VPS it is blocked by the parsing server.

main3.py is a variant of main2.py but using ThreadPoolExecutor as in the main.py variant. The duration of parsing 3 categories of the site averages 25 minutes. Works with remarks - periodically parsing completes without result. The reason for the problems may be that the proxy service scrapeops.io allows only one Thread. Gave up using this variant.