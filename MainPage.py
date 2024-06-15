import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from CellValues import CellValues


def main():
    driver = setup_driver()
    driver.get("https://sudokuhit.com/ru/")
    copy_board(driver)


def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def copy_board(driver):
    board = [[0 for col in range(9)] for row in range(9)]

    highlighted_value = driver.find_elements(By.XPATH,
                                             "//td[@class='game-cell game-value cell-selected highlight-number highlight-table'] |  //td[@class='game-cell game-value highlight-number']  |  //td[@class='game-cell game-value highlight-number'] ")
    other_values = driver.find_elements(By.XPATH,
                                        "//table//td[@class='game-cell game-value'] | //td[@class='game-cell game-value highlight-table']")

    for element in highlighted_value:
        elem_row, elem_col, elem_value = get_indexes_and_values(element)
        board[elem_row][elem_col] = elem_value
    for element in other_values:
        elem_row, elem_col, elem_value = get_indexes_and_values(element)
        board[elem_row][elem_col] = elem_value
    print(board)


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
    numeric_values = list(CellValues.cell_values.keys())

    if element.text == " ":
        value = '0'
    else:
        pattern_value = re.compile(r'd=\"(.*)\"></path>')
        value_result = pattern_value.search(html).group(1)
        value = numeric_values[list(CellValues.cell_values.values()).index(value_result)]
    return int(row), int(column), int(value)


# start


main()
# copy board

# solve

# fill on site
