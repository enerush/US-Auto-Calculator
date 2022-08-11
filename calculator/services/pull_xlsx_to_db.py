import sqlite3
from openpyxl.reader.excel import load_workbook
from datetime import date


def pull_to_db(xlsx_file: str):
    book = load_workbook(xlsx_file)
    sheet = book.active
    rows = sheet.rows

    conn = sqlite3.connect('../../../db.sqlite3')
    cursor = conn.cursor()

    for row in rows:
        auction, city, seaport, price = row
        cursor.execute(f'''INSERT INTO calculator_city(
                        auction, city, seaport, price, last_update) 
                        VALUES 
                        ("{auction.value}", "{city.value}", "{seaport.value}", "{price.value}", "{date.today()}")''')

    conn.commit()
    conn.close()


pull_to_db('prices.xlsx')