import time
import Web

from Sudoku import solve


def main():
    driver = Web.setup_driver()
    driver.get("https://sudokuhit.com/ru/")
    board = Web.copy_board(driver)
    solve(board)
    Web.fill_board(driver, board)
    time.sleep(10)


main()
