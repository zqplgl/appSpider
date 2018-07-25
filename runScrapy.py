from scrapy import cmdline
def run():
    cmdline.execute("scrapy crawl google_play".split())

if __name__=="__main__":
    run()