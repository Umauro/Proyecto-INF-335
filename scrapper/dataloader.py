import pandas as pd
from db import do_sql_upsert, USER_DATA, BD_DATA 

GAMES_UPSERT = '''
INSERT INTO public.games(
        permalink,
        title,
        price,
        image,
        url,
        description)
    VALUES {} 
    ON CONFLICT ON CONSTRAINT games_pkey 
        DO UPDATE 
        SET price = EXCLUDED.price,
            url = EXCLUDED.url,
            description = EXCLUDED.description
'''

PRICES_INSERT = '''
INSERT INTO public.price(
        permalink,
        date,
        price)
        VALUES {}
'''

class DataLoader:
    def __init__(self,df):
        self.df = df
        
    def upsert_games(self,upsert_query):
        try:
            df_aux = self.df[['permalink','title','price','image','url','description']]
            values = [
                # reemplazar " por ' para casos con ' en el email
                "{}".format(value).replace(r'"', r"'")
                if value else 'NULL'
                for value in df_aux.itertuples(
                    index=False,
                    name=None)
            ]
            if do_sql_upsert(
                USER_DATA,
                BD_DATA,
                upsert_query.format(
                    ','.join(values).replace('None', 'NULL')
                )  # Es necesario reemplazar None por NULL en la consulta
            ):
                print(
                    "Juegos insertados y/o actualizados")
            else:
                raise Exception('Error en do_sql_upsert')
        except Exception as error:
            print(
                "Error en upload_data: {}".format(
                    repr(error)
                )
            )
            
    def insert_price(self,insert_query):
        try:
            self.df.date = self.df.date.astype(str)
            df_aux = self.df[['permalink','date','price']]
            
            values = [
                # reemplazar " por ' para casos con ' en el email
                "{}".format(value).replace(r'"', r"'")
                if value else 'NULL'
                for value in df_aux.itertuples(
                    index=False,
                    name=None)
            ]
            
            if do_sql_upsert(
                USER_DATA,
                BD_DATA,
                insert_query.format(
                    ','.join(values).replace('None', 'NULL')
                )):
                print(
                    "Precios insertados")
            else:
                raise Exception('Error en do_sql_upsert')
        except Exception as error:
            print('Error en insert_price')