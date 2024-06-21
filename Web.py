import re

from selenium import webdriver
from selenium.webdriver.common.by import By

from Sudoku import cell_values

HIGHLIGHTED_VALUES = "//td[@class='game-cell game-value cell-selected highlight-number highlight-table'] |  //td[@class='game-cell game-value highlight-number']"
OTHER_VALUES = "//td[@class='game-cell game-value highlight-table'] |//td[@class='game-cell game-value']"


def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def copy_board(driver):
    board = [[0 for col in range(9)] for row in range(9)]

    highlighted_values = driver.find_elements(By.XPATH,
                                              HIGHLIGHTED_VALUES)
    other_values = driver.find_elements(By.XPATH,
                                        OTHER_VALUES)

    for element in highlighted_values:
        elem_row, elem_col, elem_value = get_indexes_and_values(element)
        board[elem_row][elem_col] = elem_value
    for element in other_values:
        elem_row, elem_col, elem_value = get_indexes_and_values(element)
        board[elem_row][elem_col] = elem_value
    return board


def get_indexes_and_values(element):
    html = element.get_attribute('outerHTML')

    # get row
    pattern_row = re.compile(r'data-row=\"(\d)\"')
    row_result = pattern_row.search(html)
    row = row_result.group(1)

    # get column
    pattern_col = re.compile(r'data-col=\"(\d)\"')
    column_result = pattern_col.search(html)
    column = column_result.group(1)

    # get value
    numeric_values = list(cell_values.keys())

    if element.text == " ":
        value = '0'
    else:
        pattern_value = re.compile(r'd=\"(.*)\"></path>')
        value_result = pattern_value.search(html).group(1)
        value = numeric_values[list(cell_values.values()).index(value_result)]
    return int(row), int(column), int(value)


def fill_board(driver, board):
    empty_values = driver.find_elements(By.XPATH, "//td[@class='game-cell highlight-table'] | //td[@class='game-cell']")

    for element in empty_values:
        elem_row, elem_col, elem_value = get_indexes_and_values(element)
        element.click()
        elem_value = board[elem_row][elem_col]
        value_locator = "//div[@data-value='{}']".format(str(elem_value))
        web_elem = driver.find_element(By.XPATH, value_locator)
        web_elem.click()
