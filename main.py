from scrappers.common import ScrapperService
from scrappers.dou_scrapper import DouScrapper

def main():
    scrapper = ScrapperService()
    scrapper.register(DouScrapper())
    scrapper.run()


if __name__ == "__main__":
    main()