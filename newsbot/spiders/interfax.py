import datetime

from newsbot.spiders.news import NewsSpider, NewsSpiderConfig


class InterfaxSpider(NewsSpider):
    name = "interfax"

    start_urls = ["https://www.interfax.ru/news/{}".format(datetime.datetime.today().strftime("%Y/%m/%d"))]
    config = NewsSpiderConfig(
        title_path='//h1[contains(@itemprop, "headline")]/text()',
        date_path='//meta[contains(@property, "published_time")]/@content',
        date_format="%Y-%m-%dT%H:%M%z",
        text_path='//article[contains(@itemprop, "articleBody")]/p[not(contains(@itemprop, "author"))]//text()',
        topics_path='//aside[contains(@class, "textML")]/a//text()',
        authors_path='//p[contains(@itemprop, "author")]//text()',
        reposts_fb_path="_",
        reposts_vk_path="_",
        reposts_ok_path="_",
        reposts_twi_path="_",
        reposts_lj_path="_",
        reposts_tg_path="_",
        likes_path="_",
        views_path="_",
        comm_count_path="_",
    )

    def parse(self, response):
        page_date = datetime.datetime.today().date()

        while page_date >= self.until_date:
            url = "https://www.interfax.ru/news/" + page_date.strftime("%Y/%m/%d")
            yield response.follow(url, self.parse_page)

            page_date -= datetime.timedelta(days=1)

    def parse_page(self, response):
        url = response.url
        page = int(url.split("page_")[-1]) if "page_" in url else 0
        for page_href in response.xpath('//div[contains(@class, "pages")]/a/@href').extract():
            if page != 0:
                continue
            yield response.follow(page_href, self.parse_page)
        for document_href in response.xpath('//div[contains(@class, "an")]/div/a/@href').extract():
            yield response.follow(document_href, self.parse_document)
