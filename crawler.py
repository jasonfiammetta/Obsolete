import time
import requests
from bs4 import BeautifulSoup
from config import crawl_speed, letter, base_url, out
from pathlib import Path


def crawl():
    page = 1

    def get_url():
        return f"{base_url}/list/{letter}/{page}"

    def flatten(list_of_list):
        return [item for sublist in list_of_list for item in sublist]

    pages = []
    r = requests.get(get_url())
    # while r:
    now = time.time()
    while page < 5:
        pages.append(BeautifulSoup(r.text, 'html.parser'))
        time.sleep(crawl_speed)
        print(f'{letter} page {page}')
        page += 1
        r = requests.get(get_url())
    print(f'finished; {page - 1} pages found in {time.time() - now} seconds')

    list_az = []
    for p in pages:
        uls = filter(lambda x: 'data-testid' in x.attrs, p.find_all('ul'))
        for ul in uls:
            list_az.append(ul)

    flat_everything = []
    for az in list_az:
        flat_everything += list(map(lambda x: x.find_all('a')[0], az.find_all('li')))

    print(f"words starting with {letter}: {len(flat_everything)}")

    record = list(map(lambda x: f"{x.string}: {x.attrs['href']}\n", flat_everything))
    just_links = list(map(lambda x: x.attrs['href'], flat_everything))

    p = Path(out)
    p.mkdir(exist_ok=True)
    file = (p / f"{letter}.txt").open("a")
    # file = open(fr"wordsByLetter/{letter}.txt", "a")
    for a in record:
        file.write(a)

    return just_links

