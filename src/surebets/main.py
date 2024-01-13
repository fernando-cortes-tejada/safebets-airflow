import os
import pandas as pd
from datetime import datetime, timedelta
from src.utils import send_message
from src.surebets import utils
from src.surebets.bet365.main import scrape as scrape_bet365
from src.surebets.betano.main import scrape as scrape_betano
from src.surebets.chuntala.main import scrape as scrape_chuntala
from src.surebets.pinnacle.main import scrape as scrape_pinnacle
from src.surebets.teapuesto.main import scrape as scrape_teapuesto


# send a message to the telegram group when the DAG starts
def trigger(**kwargs) -> str:
    league = kwargs["league"]
    # category = kwargs["category"]
    websites = kwargs["websites"]
    datetime_ = (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    # msg = f"Triggering {website.upper()}, {league.upper()}:{category} at {datetime_}"
    msg = f"Triggering {', '.join(websites).upper()}, {league.upper()} at {datetime_}"
    return send_message(msg)


# scraper
def scrape(**kwargs) -> None:
    league = kwargs["league"]
    # category = kwargs["category"]
    timeout = kwargs["timeout"]
    website = kwargs["website"]

    # get the current datetime
    dt_ini = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # initialize the flags for scraping
    flag = True
    i = 0
    while flag:
        try:
            # call the scraping function
            match website:
                case "bet365":
                    df = scrape_bet365(league, dt_ini, timeout)
                case "betano":
                    df = scrape_betano(league, dt_ini, timeout)
                case "chuntala":
                    df = scrape_chuntala(league, dt_ini, timeout)
                case "pinnacle":
                    df = scrape_pinnacle(league, timeout)
                case "teapuesto":
                    df = scrape_teapuesto(league, dt_ini, timeout)
        except ValueError as e:
            # inform if the scraping failed
            send_message(f"{website.upper()} ({league.upper()}) failed")
            print(str(e))
        else:
            try:
                if len(df) > 0:
                    msg = f"{website.upper()} ({league.upper()}) OK - {len(df)} records"
                    send_message(msg)
                    flag = False
                elif i > 0:
                    msg = f"{website.upper()} ({league.upper()}) - 0 records"
                    send_message(msg)
                    flag = False
                filename = f"src/data/scraped_df/{website}_{league}.csv"
                df.to_csv(filename, index=False)
            except ValueError as e:
                print(str(e))
            i += 1


# calculate the surebets and send a message to the telegram group if there is one
def calculate(**kwargs) -> None:
    league = kwargs["league"]
    # category = kwargs["category"]
    websites = kwargs["websites"]

    lst = []
    for website in websites:
        # read the scraped data (it is a file that is going to be deleted after the calculation)
        df = pd.read_csv(f"src/data/scraped_df/{website}_{league}.csv")
        lst.append(df.to_dict(orient="records"))

    # the number of scraped websites
    # n = len(lst)

    # sb = []
    # calculate the surebets
    # for i in range(n - 1):
    # for j in range(i + 1, n):
    # sb += utils.get_surebet(lst[i], lst[j])

    # create a dataframe with the surebets
    # df = pd.DataFrame(sb)

    # send a message to the telegram group if there is a surebet
    if len(df) > 0:
        send_message(f"Scraped {len(df)} records on pinnacle")
        # df = utils.calculate_profit_df(df)
        # df = utils.generate_message(df)
        # for text in df["text"].values:
        # send_message(text)
        # send_message(text, chat_id="-906130924")
        # send_message(text, chat_id=794589367)
        # send_message(text, chat_id=5280791759)
    else:
        send_message(f"No surebets ({league.upper()})")


# delete the scraped data
def clean(**kwargs) -> None:
    league = kwargs["league"]

    # find the files and delete them
    for file in os.listdir("src/data/scraped_df"):
        if file.endswith(f"{league}.csv"):
            os.remove(os.path.join("src/data/scraped_df", file))
