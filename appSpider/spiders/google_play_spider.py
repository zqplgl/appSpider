import re
from scrapy import Request,FormRequest
from scrapy.spiders import Spider
from bs4 import BeautifulSoup
from ..items import AppspiderItem
import scrapy

class googleplaySpider(Spider):
    name = 'google_play'
    urls = ['https://play.google.com/store/apps', 'https://play.google.com/store/apps/top',
                    'https://play.google.com/store/apps/new']

    see_more_urls = []
    app_urls = []
    def start_requests(self):
        for url in self.urls:
            yield  Request(url,callback=self.get_see_more_requests)

    def parse_nbp(self,r):
        data = {}
        info = re.findall(r";var nbp=(.+?);var", r.text)[-1]

        if info == "''":
            return None, None
        infos = info.replace("\\x22", '').replace("\\\\u003d", "=").split("[")[1].split("]")[0].split(",")

        url = infos[0]
        if infos[1]!="null":
            data["pagTok"] = infos[1]
        if infos[2]!="null":
            data["num"] = infos[2]
        if infos[3]!="null":
            data["start"] = infos[3]
        if infos[4]!="null":
            data["numChildren"] = infos[4]
        if infos[5]!="null":
            data["ipf"] = infos[5]
        if infos[6]!="null":
            data["clp"] = infos[6]
        if infos[7]!="null":
            data["pagtt"] = infos[7]

        return url, data

    def get_app_requests(self,r):
        requests = []
        app_urls = BeautifulSoup(r.text, 'lxml').find_all('span', class_="preview-overlay-container")
        app_url_prefix = "https://play.google.com/store/apps/details?id="
        app_urls = [app_url_prefix+app_url["data-docid"] for app_url in app_urls]

        for app_url in app_urls:
            requests.append(Request(url=app_url,callback=self.get_app_info))
        self.app_urls.extend(app_urls)
        print("app_urls_num: ",len(set(self.app_urls)))
        print("see_more_urls_num: ", len(self.see_more_urls))
        url, data = self.parse_nbp(r)
        if url != None:
            requests.append(FormRequest(url=url, formdata=data, callback=self.get_app_requests))

        return requests

    def get_see_more_requests(self, r):
        requests = []
        root_url = r'https://play.google.com'
        see_more_urls = BeautifulSoup(r.text, 'lxml').find_all('a', text="See more")
        see_more_urls = [root_url+tempurl["href"] for tempurl in see_more_urls]
        self.see_more_urls.extend(see_more_urls)
        for see_more_url in see_more_urls:
            requests.append(Request(url=see_more_url,callback=self.get_app_requests))
        print("see_more_urls: ",len(self.see_more_urls))
        url,data = self.parse_nbp(r)

        if url!=None:
            requests.append(FormRequest(url=url, formdata=data, callback=self.get_see_more_requests))

        return requests

    def get_app_info(self,r):
        app_info = AppspiderItem()

        #******************app_id*********************1
        app_info["app_id"] = r.url.split("id=")[1]

        mainhtml = BeautifulSoup(r.text, 'lxml')

        # *****************rate_* and num_comments*************2-8
        ratings = mainhtml.find_all('div', class_="K9wGie")
        if len(ratings) != 1:
            app_info["rating"] = None
            app_info["num_comments"] = None
            for i in range(1,6):
                app_info["rate_%s" % i] = None
        else:
            rates = mainhtml.find_all("div",class_="mMF0fd")
            for rate in rates:
                spans = rate.find_all("span")
                app_info["rate_%s" % spans[0].text] = spans[1]["title"].replace(",","")
            app_info["rating"] = ratings[0].find(class_="BHMmbe").text
            app_info["num_comments"] = ratings[0].find("span", class_="EymY4b").find(class_="").text.replace(",","")

        # *************************name**********************9
        names = mainhtml.find_all("h1", class_="AHFaub", itemprop="name")
        app_info['name'] = names[0].span.text if len(names) == 1 else None

        # *************************developer and category********************10,11
        dev_cat = mainhtml.find_all("span", class_=['T32cc', 'UAO9ie'])
        app_info["developer"] = dev_cat[0].text if len(dev_cat) else None
        category = []
        for cat in dev_cat[1:]:
            category.append(cat.text)
        app_info["category"] = None if len(category) == 0 else category

        # ************************new****************************12
        content = mainhtml.find_all("c-wiz", jsrenderer="FzdkFd")
        if len(content) != 1:
            app_info["new"] = None
        else:
            content = content[0].find_all("content", class_="")
            app_info["new"] = content[0].text if len(content) == 1 else None

        # *****************************description**************13
        description = mainhtml.find_all("meta", itemprop="description")
        app_info["description"] = description[0]["content"] if len(description) == 1 else None

        # **********************other**************************14-21
        add_info = mainhtml.find_all("div", class_="hAyfc")

        for info in add_info:
            if info.div.text == "Size":
                app_info["size"] = info.span.text
            elif info.div.text == "Installs":
                app_info["installs"] = info.span.text
            elif info.div.text == "Current Version":
                app_info["version"] = info.span.text
            elif info.div.text == "In-app Products":
                app_info["charge"] = info.span.text
            elif info.div.text == "Updated":
                app_info["updated"] = info.span.text
            elif info.div.text == "Developer":
                temp = info.span.div.span
                divs = temp.find_all("div")
                for div in divs:
                    if div.a==None:
                        app_info["address"] = div.text
                    elif div.a.text=="Visit website":
                        app_info["website"] = div.a["href"]
                    elif "@" in div.a.text and ".com" in div.a.text:
                        app_info["email"] = div.a.text


        print ("app_info",app_info)