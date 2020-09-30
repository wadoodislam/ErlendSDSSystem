import csv

import bs4
import requests


def scrape():
    csvwriter = csv.writer(open('kulzer.csv', 'w'))
    csvwriter.writerow(["title", "url"])

    data = {
        'AjaxAction': 'GetDownloads',
        'types': 143552,
        'brands': '',
        'products': '',
        'text': ''
    }

    soup = bs4.BeautifulSoup(requests.post('https://www.kulzer.com/en/int/downloads_5/downloads.aspx', data=data, verify=False).text.replace("\r", "").replace("\n", ""), 'lxml')
    for sheet in soup.findAll("div", {"class": "dl-item-container clearfix"}):
        if sheet.get('data-langcode') == 'norwegian':
            soup2 = bs4.BeautifulSoup(str(sheet), 'lxml')
            title = soup2.find("span", {"class": "dl-item-title"}).text.strip().split("/", 1)

            for child in sheet.children:
                if type(child) == bs4.element.Tag:
                    if child.get("href"):
                        url = child.get("href")

            csvwriter.writerow([title[0], url])


if __name__ == '__main__':
    scrape()