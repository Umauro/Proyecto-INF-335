import numpy as np
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import re

class WarpigScrapper:
    def __init__(self, base_url='https://www.warpig-games.cl/15-juegos-de-mesa'):
        self.base_url = base_url
        self.board_game_list = list()

    def get_next_page_url(self,page_url='https://www.warpig-games.cl/15-juegos-de-mesa'):
        try:
            if page_url == self.base_url:
                url = urllib.request.urlopen(
                    "{}".format(
                        self.base_url
                    )
                )
            else:
                url = urllib.request.urlopen(
                    "{}".format(page_url)
                )
            soup = BeautifulSoup(url,'html.parser')
            next_div = soup.find(
                "div",
                {"class":"bottom-pagination-content clearfix"}
            )
            next_url = next_div.find(
                "a",
                {"title":"Siguiente"}
            ).get('href')
            next_url = self.base_url.replace("/15-juegos-de-mesa", next_url)
            return next_url
        except AttributeError as error:
            return None
        except Exception as error:
            print(
                "Error al obtener la siguiente página: {}".format(
                    repr(error)
                )
            )
            return None

    def get_products_url(self,page_url):
        try:
            url = urllib.request.urlopen(
                "{}".format(page_url)
            )
            soup = BeautifulSoup(url,'html.parser')
            products_url = [url.get('href') for url in soup.find_all(href=re.compile("/juegos-de-mesa/"))]
            return list(set(products_url))
        except Exception as error:
            print(
                "Error en get_products_url: {}".format(
                repr(error)
                )
            )
            return None

    def get_product_info(self, page_url):
        try:
            url = urllib.request.urlopen(
                '{}'.format(
                    page_url
                )
            )
            soup = BeautifulSoup(url,'html.parser')

            #delete strong tags
            for tag in soup.find_all('strong'):
                tag.replaceWith('')
            for tag in soup.find_all('b'):
                tag.replaceWith('')
            for tag in soup.find_all('i'):
                tag.replaceWith('')
            for tag in soup.find_all('em'):
                tag.replaceWith('')

            #get image
            product_dict = dict()
            image_div = soup.find('div',{'id':'image-block'})
            product_dict['image'] = image_div.img.get('src')

            #get title and Price
            summary_div = soup.find('div',{'class':'pb-center-column col-xs-12 col-sm-5 col-md-5'})
            product_dict['title'] = summary_div.h1.contents[0]
            product_dict['price'] = summary_div.find('div',{'class':'price_box clearfix'}).find('span',{'itemprop':'price'}).contents[0]

            #get description
            description_div = soup.find(
                'div',
                {'id':'more_info_block'}
            ).find(
                'div',
                {'class':'rte'}
            )

            if description_div != None:
                for tag in description_div.find_all('span'):
                    tag.replaceWith('')
                for tag in description_div.find_all('a'):
                    tag.replaceWith('')
                for tag in description_div.find_all('iframe'):
                    tag.replaceWith('')


                description_p = [
                    description.getText()
                    for description in description_div.findAll('p')
                ]

                product_dict['description'] = '\n '.join(description_p).replace(r'"','')
            else:
                product_dict['description'] = 'Descripción no proporcionada.'
            product_dict['url'] = page_url
            self.board_game_list.append(product_dict)

        except Exception as error:
            print(page_url)
            print(error)

    def recursive_scrapper(self,page_url):
        urls = self.get_products_url(page_url)
        for product_url in urls:
            self.get_product_info(product_url)
        next_url = self.get_next_page_url(page_url)
        if next_url:
            print("Next Page: {}".format(next_url))
            return self.recursive_scrapper(next_url)
        else:
            return

    def get_contents(self):
        try:
            self.recursive_scrapper(self.base_url)
            df = pd.DataFrame(self.board_game_list)
            df['date'] = datetime.datetime.today()
            return df
        except Exception as error:
            print(
                "Error en get_context: {}".format(
                    repr(error)
                )
            )
            return None

class WarpigTransformer:
    def __init__(self,df):
        self.df = df
    def create_permalink(self):
        self.df['permalink'] = 'skyship-'+ self.df.title.str.replace(' ','-')
    def clean_date(self):
        self.df.date = self.df.date.dt.date
    def clean_price(self):
        self.df.price = self.df.price.str.replace(u'\xa0', u' ')
        self.df.price = self.df.price.str.replace(r'\$','').replace('.','')
        self.df.price = self.df.price.str.replace('.','')
        self.df.price = self.df.price.astype(int)
    def fill_description(self):
        self.df.description.fillna('SIN DESCRIPCIÓN',inplace=True)

    def clean_description(self):
        self.df.description = self.df.description.str.replace(u"\u201c",r'',regex=True)
        self.df.description = self.df.description.str.replace(u"\u201d",r'',regex=True)
        self.df.description = self.df.description.str.replace(u"\u2026",r'',regex=True)
        self.df.description = self.df.description.str.replace(u"\u2019",r'',regex=True)
        self.df.description = self.df.description.str.replace(u"\u2014",r'',regex=True)
        self.df.description = self.df.description.str.replace(u"\u0155",r'',regex=True)
        self.df.description = self.df.description.str.replace(u"\u0155",r'',regex=True)
        self.df.description = self.df.description.str.replace(r"\xa0",r'',regex=True)
        self.df.description = self.df.description.str.replace(r"\'","''",regex=True)
    def drop_duplicates(self):
        self.df.drop_duplicates('permalink',keep='first',inplace=True)

    def transform_data(self):
        self.create_permalink()
        self.clean_date()
        self.clean_price()
        self.fill_description()
        self.drop_duplicates()
        self.clean_description()
        return self.df
