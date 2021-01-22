import logging

from scrapy import Spider, Request

from dateutil import parser

from Gideon.database.database import Database
import params
from Gideon.database.models import Newspaper


class EPatrika(Spider):
    name = 'epatrika'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.db = Database(params.db_url)

    def start_requests(self):
        newspapers = [
            'the_hindu',
            'livemint',
            'times_of_india',
            'economic_times',
            'hindustan_times',
            'deccan_chronicle',
        ]
        for newspaper in newspapers:
            yield Request(
                method='GET',
                url=f'https://epatrika.website/show-editions.php?newspaper={newspaper}',
                callback=self.get_editions,
                meta={'newspaper': newspaper}
            )

    def get_editions(self, response):
        newspaper = response.meta['newspaper']

        ul = response.css('ul.collection li.collection-item')
        for li in ul:

            edition = None
            language = None

            properties = li.xpath('./p/text()').extract()
            for prop in properties:
                prop_split = prop.split(':')
                key = prop_split[0].strip().lower()
                value = prop_split[1].strip().lower()

                if key == 'edition':
                    edition = value

                if key == 'language':
                    language = value

            link = li.xpath('./a[1]/@href').extract_first()
            link = response.urljoin(link)

            yield Request(
                method='GET',
                url=link,
                callback=self.get_days,
                meta={'newspaper': newspaper, 'edition': edition, 'language': language}
            )

    def get_days(self, response):
        newspaper = response.meta['newspaper']
        edition = response.meta['edition']
        language = response.meta['language']

        ul = response.css('ul.collection li.collection-item')
        for li in ul:
            date = li.xpath('./p[1]/text()').extract_first()
            date = date.replace(':', '').strip()
            date = parser.parse(date)

            language_for_day = li.xpath('./p[2]/text()').extract_first()
            language_for_day = language_for_day.replace(':', '').strip().lower()

            title = li.xpath('./span/a[1]//text()').extract_first().strip().lower()

            paper_type = 'none'
            if 'editorial' in title:
                paper_type = 'editorial'
            elif 'magazine' in title:
                paper_type = 'magazine'
            elif 'adfree' in title:
                paper_type = 'adfree'

            link = li.xpath('.//a[1]/@href').extract_first()
            newspaper_obj = self.db.session.query(Newspaper).filter_by(
                name=newspaper,
                edition=edition,
                language=language_for_day,
                type=paper_type,
                timestamp=date
            ).one_or_none()

            if newspaper_obj is None:
                newspaper_obj = Newspaper(
                    name=newspaper,
                    edition=edition,
                    language=language_for_day,
                    type=paper_type,
                    timestamp=date,
                    link=link,
                    drive_file_id='NONE'
                )
                self.db.session.add(newspaper_obj)

            # THIS SHOULDN'T BE NEEDED UNLESS I MESS UP, SO LEAVING IT HERE FOR EMERGENCIES
            # else:
            #     self.db.session \
            #         .query(Newspaper) \
            #         .filter_by(id=newspaper_obj.id) \
            #         .update({'link': link})

    def get_paper(self, link):
        pass

    def parse(self, response, **kwargs):
        self.log('Default callback method called.', logging.DEBUG)

    def close(self, spider):
        self.db.session.commit()
        self.db.session.close()
