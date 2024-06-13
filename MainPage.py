import time

from selenium import webdriver


def main():
    driver = setup_driver()
    driver.get("https://sudokuhit.com/ru/")


def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


main()
