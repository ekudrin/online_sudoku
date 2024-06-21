import re
import time
import Web

from Sudoku import Sudoku


def main():
    driver = Web.setup_driver()
    driver.get("https://sudokuhit.com/ru/")
    board = Web.copy_board(driver)
    print(board)
    sudoku = Sudoku()
    sudoku.solve(board)
    Web.fill_board(driver, board)
    time.sleep(10)


main()
