import json

from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.common.exceptions import TimeoutException

result = []

for i in range(1, 100):

    RETRIES = 3

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)

    url = 'https://www.climatempo.com.br/climatologia/{}/city'.format(i)
    print(url)

    driver.set_page_load_timeout(20)
    for j in range(1, RETRIES):
        try:
            driver.get(url)
            time.sleep(10)

        except TimeoutException:
            print("Timeout, Retrying... (%(i)s/%(max)s)" % {'i': j, 'max': RETRIES})
            continue

        else:
            city_span = driver.find_element_by_class_name('name-city-prev-home')
            city_spans = city_span.find_elements_by_tag_name('span')
            city_name = city_spans[1].get_attribute('innerHTML')

            table = driver.find_elements_by_tag_name('table')
            html = table[1].get_attribute("innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            tbody = soup.select_one("tbody")
            data = [d for d in tbody.select("tr")]

            month_list = []
            for item in data:
                td = item.select("td")
                month_list.append({'month': td[0].text,
                                   'min': td[1].text,
                                   'max': td[2].text,
                                   'precipitation': '{} mm'.format(td[3].text)})

            result.append({'city': city_name, 'climatology': month_list})
            driver.quit()
            break


with open('src/result.json', 'w') as data_file:
    json.dump(result, data_file, ensure_ascii=False)

