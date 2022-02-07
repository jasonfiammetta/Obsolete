import time
import requests
from bs4 import BeautifulSoup
from config import crawl_speed, letter, scrape_url, verbose, out, archaic_folder
from pathlib import Path
import asyncio

archaic_words = []


def is_archaic(word):
    arc = word.find_all("span", {"class": "luna-label"})
    if arc:
        return arc[0].string == 'Archaic'
    return False


async def parse_worker(queue):
    offset = len(scrape_url)

    while True:
        [future, link] = await queue.get()
        r = await future
        word_page = BeautifulSoup(r.text, 'html.parser')
        if is_archaic(word_page):
            archaic_words.append(link)
            if verbose:
                print(f"archaic: {link[offset:]}")

        queue.task_done()


async def scrape(links):
    queue = asyncio.Queue()
    tasks = []
    start = now = time.time()
    for index, link in enumerate(links):
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, requests.get, link)
        queue.put_nowait([future, link])
        task = asyncio.create_task(parse_worker(queue))
        tasks.append(task)

        if verbose and not index % 100:
            print(f"{index} words scraped in {time.time() - now} seconds")
            now = time.time()
        time.sleep(crawl_speed)

    await queue.join()

    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

    print(f'finished; {len(archaic_words)} archaic words found in {time.time() - start} seconds')

    p = Path(out) / Path(archaic_folder)
    p.mkdir(exist_ok=True)
    file = (p / f"{letter}.txt").open("a")
    for a in archaic_words:
        file.write(a + "\n")
