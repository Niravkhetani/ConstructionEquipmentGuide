import scrapy


class Scrapy_login(scrapy.Spider):

    name        = "login"

    def start_requests(self):
        return [scrapy.FormRequest("http://quotes.toscrape.com/login",
                                    formdata={'user':"one","password":"one"},
                                    callback=self.loged_in)]


    def loged_in(self,response):
        pass