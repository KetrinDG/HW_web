from beautiful_soup import parser_lxml
from src import seeds
from my_scrapy.my_scrapy.spiders import start_scrapy

if __name__ == "__main__":
    while True:
        print("\033[032m---------------------------------------------------\033[0m")
        print("\033[036mChoice a method for scraping:\033[0m")
        print("\033[033m1 - Beautiful soup")
        print("2 - Scrapy")
        print("\033[034mexit - Exit\033[0m")
        print("\033[032m---------------------------------------------------\033[0m")
        cmd = input("\033[036mCommand: ")
        print(cmd)
        match cmd:
            case "1":
                print("\033[034mLoading...")
                parser_lxml()
                seeds()
                print("\033[032mDone.")
            case "2":
                print("\033[034mLoading......")
                start_scrapy()
                seeds()
                print("\033[032mDone.")
            case "exit":
                print("\033[036mGoodby!")
                quit()
            case _:
                print("\033[035mUnknown command\033[0m")
