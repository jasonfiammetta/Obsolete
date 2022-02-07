import crawler
import scraper

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    words = crawler.crawl()
    # file = open(fr"letter{letter}.txt", "a")
    # for a in final:
    #     file.write(a)
    scraper.scrape(words)
