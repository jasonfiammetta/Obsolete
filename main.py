import asyncio
import crawler
import scraper


async def main():
    words = crawler.crawl()
    # file = open(fr"letter{letter}.txt", "a")
    # for a in final:
    #     file.write(a)
    await scraper.scrape(words)

if __name__ == '__main__':
    asyncio.run(main())
