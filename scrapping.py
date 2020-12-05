import csv
import io
from selenium import webdriver
from selenium.common import exceptions
import sys
import time


def get_comments(link):
    i = 0
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(link)
    driver.maximize_window()
    time.sleep(5)

    try:
        user_comments = driver.find_element_by_xpath('//*[@id="comments"]')

    except exceptions.NoSuchElementException:
        # Note: Youtube may have changed their HTML layouts for
        # videos, so raise an error for sanity sake in case the
        # elements provided cannot be found anymore.
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    driver.execute_script("arguments[0].scrollIntoView();", user_comments)
    time.sleep(7)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while i != 3:
        # Опускаем вниз до следующего лоада.
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Ждем пока загрузит все.
        time.sleep(2)

        # Рассчитываем длинну скрола.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1

    try:
        usernames = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comments = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)
    finally:
        with io.open('results.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_ALL)
            writer.writerow(["Username", "Comment"])
            for username, comment in zip(usernames, comments):
                writer.writerow([username.text, comment.text])
        driver.close()
        time.sleep(2)
        driver.quit()
