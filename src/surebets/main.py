import os
import pandas as pd
from datetime import datetime, timedelta
from ..utils import send_message
from . import utils


# send a message to the telegram group when the DAG starts
def trigger(**kwargs) -> str:
    league = kwargs["league"]
    category = kwargs["category"]
    datetime_ = (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    return send_message(f"Lanzando {league.upper()}:{category} a las {datetime_}")


# calculate the surebets and send a message to the telegram group if there is one
def calculate(**kwargs) -> None:
    league = kwargs["league"]
    category = kwargs["category"]
    # read the scraped data (it is a file that is going to be deleted after the calculation)
    df_chuntala = pd.read_csv(f"src/data/scraped_df/chuntala_{league}_{category}.csv")
    df_betano = pd.read_csv(f"src/data/scraped_df/betano_{league}_{category}.csv")

    # calculate the surebets
    df = utils.get_df_surebet(df_chuntala, df_betano)

    # send a message to the telegram group if there is a surebet
    if len(df) > 0:
        df = utils.calculate_profit_df(df)
        df = utils.generate_message(df)
        for text in df["text"].values:
            send_message(text)
            send_message(text, chat_id="-906130924")
            send_message(text, chat_id=794589367)
            send_message(text, chat_id=5280791759)
    else:
        send_message(f"No hay surebets ({league.upper()}:{category})")


# delete the scraped data
def clean(**kwargs) -> None:
    league = kwargs["league"]
    category = kwargs["category"]

    # find the files and delete them
    for file in os.listdir("src/data/scraped_df"):
        if file.endswith(f"{league}_{category}.csv"):
            os.remove(os.path.join("src/data/scraped_df", file))
