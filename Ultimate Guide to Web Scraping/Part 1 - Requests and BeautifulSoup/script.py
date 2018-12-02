import requests
from bs4 import BeautifulSoup
from time import sleep
import json
from tqdm import tqdm

pages = [
    'https://www.allsides.com/media-bias/media-bias-ratings',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=1',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=2'
]


def get_agreeance_text(ratio):
    if ratio > 3:
        return "absolutely agrees"
    elif 2 < ratio <= 3:
        return "strongly agrees"
    elif 1.5 < ratio <= 2:
        return "agrees"
    elif 1 < ratio <= 1.5:
        return "somewhat agrees"
    elif ratio == 1:
        return "neutral"
    elif 0.67 < ratio < 1:
        return "somewhat disagrees"
    elif 0.5 < ratio <= 0.67:
        return "disagrees"
    elif 0.33 < ratio <= 0.5:
        return "strongly disagrees"
    elif ratio <= 0.33:
        return "absolutely disagrees"
    else:
        return None


def scrape_allsides_tables(data):
    print('Scraping tables...')

    for page in pages:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, 'html.parser')

        rows = soup.select('tbody tr')

        for row in rows:
            d = dict()

            d['name'] = row.select_one('.source-title').text.strip()
            d['allsides_page'] = 'https://www.allsides.com' + row.select_one('.source-title a')['href']
            d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
            d['agree'] = int(row.select_one('.agree').text)
            d['disagree'] = int(row.select_one('.disagree').text)
            d['agree_ratio'] = d['agree'] / d['disagree']
            d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])

            data.append(d)

        sleep(10)
    return data


def scrape_allsides_sources(data):
    print('Scraping news source pages...')

    for d in tqdm(data):
        r = requests.get(d['allsides_page'])
        soup = BeautifulSoup(r.content, 'html.parser')

        try:
            website = soup.select_one('.www')['href']
            d['website'] = website
        except TypeError:
            pass

        sleep(10)
    return data


def save_json(data):
    with open('allsides.json', 'w') as f:
        json.dump(data, f)


def open_json():
    with open('allsides.json', 'r') as f:
        return json.load(f)


def main():
    data = []
    data = scrape_allsides_tables(data)
    data = scrape_allsides_sources(data)
    save_json(data)

    print('Done.')


if __name__ == '__main__':
    main()
