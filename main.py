import requests
import selectorlib
import time
import sqlite3
from send_email import send_email


URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


def scrape(url):
    """ Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    """ Extracts the value of the source inside specific CSS selectors"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]

    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                email_message = f"""\
Subject: Hey, new event was found!
The following even was found:
{extracted}
"""
                store(extracted)
                send_email(message=email_message)
        time.sleep(2)