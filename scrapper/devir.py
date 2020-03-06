import numpy as np
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import re


class DevirScrapper():
    
    def __init__(self,base_url='https://devir.cl/categoria/juegos-de-mesa/'):
        self.base_url = base_url
        self.board_game_list = list()
        
    def get_next_page_url(self,page_url='https://devir.cl/categoria/juegos-de-mesa/'):
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
            next_url = soup.find(
                "a",
                {"class":"next page-numbers"}
            ).get('href')
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
            products_url = [url.get('href') for url in soup.find_all(href=re.compile("/producto/"))]
            return list(set(products_url))
        except Exception as error:
            print(
                "Error en get_products_url: {}".format(
                    repr(error)
                )
            )
            return None
    
    def get_product_info(self,page_url):
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
            
            product_dict = dict()
            
            #get image
            image_div = soup.find('div',{'class':'product-image-slider owl-carousel show-nav-hover has-ccols ccols-1'})
            product_dict['image'] = image_div.img.get('src')
            
            
            
            #get title and price
            #summary_div = soup.find('div',{'class':'summary entry-summary col-md-6'})
            #print(summary_div)
            product_dict['title'] = soup.find(
                'h2',
                {'class':'product_title entry-title show-product-nav'}
                ).contents[0].replace(
                    '(',
                    ''
                    ).replace(
                        ')',
                        ''
                        )
            
            product_dict['price'] = soup.find(
                'span',
                {'class':'woocommerce-Price-amount amount'}
                ).contents[1].replace('.','')
            
            
            #get description
            description_div = soup.find(
                'div',
                {'id':'tab-description'}
            )
                            
            if description_div != None:
                for tag in description_div.find_all('span'):
                    tag.replaceWith('')
                for tag in description_div.find_all('a'):
                    tag.replaceWith('')
                for tag in description_div.find_all('iframe'):
                    tag.replaceWith('')
                
                
                description_p = [
                    description.contents[0] 
                    for description in description_div.findAll('p') 
                ] 


                product_dict['description'] = '\n '.join(description_p)
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

class DevirTransformer:
    def __init__(self,df):
        self.df = df
    def create_permalink(self):
        self.df['permalink'] = 'devir-'+ self.df.title.str.replace(' ','-')
    def clean_date(self):
        self.df.date = self.df.date.dt.date
    def fill_description(self):
        self.df.description.fillna('SIN DESCRIPCIÓN',inplace=True)
    def drop_duplicates(self):
        self.df.drop_duplicates('permalink',keep='first',inplace=True)
    
    def transform_data(self):
        self.create_permalink()
        self.clean_date()
        self.fill_description()
        self.drop_duplicates()
        return self.df
            