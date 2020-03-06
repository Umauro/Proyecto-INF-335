from devir import DevirScrapper, DevirTransformer
from dataloader import DataLoader, GAMES_UPSERT, PRICES_INSERT

devir_scrapper = DevirScrapper()
df_devir = devir_scrapper.get_contents()
devir_transformer = DevirTransformer(df_devir)
df_devir = devir_transformer.transform_data()
devir_dataloader = DataLoader(df_devir)
devir_dataloader.upsert_games(GAMES_UPSERT)
devir_dataloader.insert_price(PRICES_INSERT)