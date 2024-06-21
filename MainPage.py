import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from CellValues import CellValues


def main():
    driver = setup_driver()
    driver.get("https://sudokuhit.com/ru/")
    board = copy_board(driver)
    solve(board)
    print(board)
    fill_board(driver, board)
    time.sleep(10)


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
    return board


def fill_board(driver, board):
    empty_values = driver.find_elements(By.XPATH, "//td[@class='game-cell highlight-table'] | //td[@class='game-cell']")

    for element in empty_values:
        elem_row, elem_col, elem_value = get_indexes_and_values(element)
        element.click()
        elem_value = board[elem_row][elem_col]
        value_locator = "//div[@data-value='{}']".format(str(elem_value))
        web_elem = driver.find_element(By.XPATH, value_locator)
        web_elem.click()


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


def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


def is_valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None


main()

# solve


# fill on site
