import requests
import selectorlib

URL = "https://programmer100.pythonanywhere.com/tours/"


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


def send_email():
    """ Sents email when a tour is listed"""
    print("Email was sent!")


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    if extracted != "No upcoming tours":
        send_email()