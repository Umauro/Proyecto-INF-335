from devir import DevirScrapper, DevirTransformer
from skyship import SkyshipScrapper, SkyshipTransformer
from warpig import WarpigScrapper, WarpigTransformer
from dataloader import DataLoader, GAMES_UPSERT, PRICES_INSERT

#devir_scrapper = DevirScrapper()
#df_devir = devir_scrapper.get_contents()
#devir_transformer = DevirTransformer(df_devir)
#df_devir = devir_transformer.transform_data()
#devir_dataloader = DataLoader(df_devir)
#devir_dataloader.upsert_games(GAMES_UPSERT)
#devir_dataloader.insert_price(PRICES_INSERT)

#skyship_scrapper = SkyshipScrapper()
#df_skyship = skyship_scrapper.get_contents()
#skyship_transformer = SkyshipTransformer(df_skyship)
#df_skyship = skyship_transformer.transform_data()
#skyship_dataloader = DataLoader(df_skyship)
#skyship_dataloader.upsert_games(GAMES_UPSERT)
#skyship_dataloader.insert_price(PRICES_INSERT)

warpig_scrapper = WarpigScrapper()
df_warpig = warpig_scrapper.get_contents()
warpig_transformer = WarpigTransformer(df_warpig)
df_warpig = warpig_transformer.transform_data()
warpig_dataloader = DataLoader(df_warpig)
warpig_dataloader.upsert_games(GAMES_UPSERT)
warpig_dataloader.insert_price(PRICES_INSERT)
