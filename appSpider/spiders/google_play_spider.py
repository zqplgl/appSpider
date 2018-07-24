import re
from scrapy import Request,FormRequest
from scrapy.spiders import Spider
from bs4 import BeautifulSoup

class googleplaySpider(Spider):
    name = 'google_play'
    root_url = r'https://play.google.com'
    urls = ['https://play.google.com/store/apps']

    seeMoreUrls = []
    a = []

    def getSeeMoreUrls(self):
        self.a.append(1)

    def start_requests(self):
        url,data = self.getNBP()
        request = FormRequest(url=url,formdata=data,callback=self.parseSeeMoreUrls)
        print request
        # for url in self.urls:
        #     yield Request(url,callback=self.parseSeeMoreUrls)

    def parseNBP(self,r):
        data = {}
        info = re.findall(r";var nbp=(.+?);var", r.text)[-1]

        if info == "''":
            return None, None
        infos = info.replace("\\x22", '').replace("\\\\u003d", "=").split("[")[1].split("]")[0].split(",")

        url = infos[0]

        data["pagTok"] = (None, infos[1]) if infos[1] != 'null' else None
        data["num"] = (None, infos[2])
        data["start"] = (None, infos[3])
        data["numChildren"] = (None, infos[4])
        data["numChildren"] = (None, infos[4])
        data["ipf"] = (None, infos[5]) if infos[5] != "null" else (None,"1")
        data["clp"] = (None, infos[6]) if infos[6] != 'null' else None
        data["pagtt"] = (None, infos[7])

        return url, data

    def getNBP(self):

        url = "https://play.google.com/store/apps?authuser=0"
        data = {}

        data["pagTok"] = "CsEBit_FqQO6AQgKEJiI5ojKLBir6uXZCRjErcygDRig6rCWCBiI1tvUBRi68dyjDRj7kNWeDBjk2KztAxiF9J7ZCBjwk_tHGOfdo6kFILix68cKIIDsrbcFIMD_vo4CIIjw5c4KIObZrLsNIO7eze4KIPu8mOsNILj23W4gsZamkgUgttbWnQgg6NSOZyDygaWnCyC27-7qBCDbiNGCDSDi-4eyDCCd7c_1AyDo2cWNDyCD2IjNBCDk09qeCCCnuvSjBBILEAoqBAgDUAmwATE=:S:ANO1ljKhC0g"
        data["num"] = "9"
        data["start"] = "9"
        data["numChildren"] = "0"
        data["ipf"] = "1"
        data["xhr"] = "1"
        data["pagtt"] = "2"

        return url,data


    def parseNBP1(self,r):
        data = {}
        info = re.findall(r";var nbp=(.+?);var", r.text)[-1]

        if info == "''":
            return None, None
        infos = info.replace("\\x22", '').replace("\\\\u003d", "=").split("[")[1].split("]")[0].split(",")

        url = infos[0]

        data["pagTok"] = infos[1] if infos[1] != 'null' else None
        data["num"] = infos[2]
        data["start"] = infos[3]
        data["numChildren"] = (None, infos[4])
        data["numChildren"] = (None, infos[4])
        data["ipf"] = (None, infos[5]) if infos[5] != "null" else (None,"1")
        data["clp"] = infos[6] if infos[6] != 'null' else None
        data["pagtt"] = infos[7]

        return url, data

    def parseSeeMoreUrls(self, r):
        all_SeeMore = BeautifulSoup(r.text, 'lxml').find_all('a', text="See more")
        self.seeMoreUrls.extend([self.root_url + tempUrl["href"] for tempUrl in all_SeeMore])
        print "seeMoreUrls: ", len(self.seeMoreUrls)
        url, data = self.parseNBP(r)
        print url,data
        # if url!=None:
        #     print url,data
        #     FormRequest(url=url,method="POST",meta=data,callback=self.parseSeeMoreUrls)

