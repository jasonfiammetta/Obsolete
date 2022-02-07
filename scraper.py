import time
import requests
from bs4 import BeautifulSoup
from config import crawl_speed, letter, scrape_url, verbose, out, archaic_folder
from pathlib import Path


def scrape(links):
    def is_archaic(word):
        arc = word.find_all("span", {"class": "luna-label"})
        if arc:
            return arc[0].string == 'Archaic'
        return False

    offset = len(scrape_url)
    archaic_words = []
    start = now = time.time()
    for index, link in enumerate(links):
        # r = requests.get(scrape_url + link)
        r = requests.get(link)
        word_page = BeautifulSoup(r.text, 'html.parser')
        if is_archaic(word_page):
            archaic_words.append(link)
            if verbose:
                print(f"archaic: {link[offset:]}")
        if verbose and not index % 100:
            print(f"{index} words scraped in {time.time() - now} seconds")
            now = time.time()
        time.sleep(crawl_speed)

    print(f'finished; {len(archaic_words)} archaic words found in {time.time() - start} seconds')

    p = Path(out) / Path(archaic_folder)
    p.mkdir(exist_ok=True)
    file = (p / f"{letter}.txt").open("a")
    for a in archaic_words:
        file.write(a + "\n")
