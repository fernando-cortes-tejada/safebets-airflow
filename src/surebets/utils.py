from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import difflib
import os

from .entities import CHROMEDRIVER_PATH

os.environ["webdriver.chrome.driver"] = CHROMEDRIVER_PATH


# the initiate driver function
def initiate_driver(prod: bool = True) -> webdriver.Chrome:
    ser = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    if prod:
        options.add_argument("--window-size=1420,1080")
        options.add_argument("--headless")
    return webdriver.Chrome(service=ser, options=options)


def initiate_driver_headless() -> webdriver.Chrome:
    ser = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1420,1080")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=ser, options=options)


def open_browser(driver: webdriver.Chrome, url: str, time_sleep: int):
    driver.get(url)
    time.sleep(time_sleep)
    print("Browser opened")


# check if the odds are a surebet
def is_surebet(odd1: float, odd2: float) -> bool:
    """Returns True if the odds are a surebet"""
    return (1.0 / odd1) + (1.0 / odd2) < 1.0


# calculate the profit of a surebet
def surebet_profit(odd1: float, odd2: float) -> float:
    """Returns the profit of a surebet"""
    return ((odd2 * odd1) / (odd1 + odd2)) - 1.0


# check for alternate name of the players on each website
# for example some players might be called "Fernando Cortés" on one website
# and on the other website "Fernando Cortes" or "Fernando Cortez" or
# "Fernando Cortés Jr." or "Fernando Cortés II", etc
def alternate_names(flawed_series: pd.Series, real_series: pd.Series) -> pd.Series:
    real_series = real_series.unique()
    return flawed_series.map(
        lambda x: difflib.get_close_matches(x, real_series, n=1, cutoff=0.8)
    ).map(lambda x: x[0] if x else None)


# we merge the two dataframes and check for surebets
def get_df_surebet(df_1: pd.DataFrame, df_2: pd.DataFrame) -> pd.DataFrame:
    nombres_alt = alternate_names(df_1["player"], df_2["player"])
    df_1["player"] = df_1["player"].mask(nombres_alt.notnull(), nombres_alt)

    df = pd.merge(df_1, df_2, "inner", on=["market", "player", "line"])

    df["surebet_1"] = df.apply(lambda x: is_surebet(x["more_x"], x["less_y"]), axis=1)
    df["surebet_2"] = df.apply(lambda x: is_surebet(x["less_x"], x["more_y"]), axis=1)
    df = df[df["surebet_1"] | df["surebet_2"]]
    return df


# calculate the profit of the surebet
def calculate_profit_df(df: pd.DataFrame) -> pd.DataFrame:
    df["profit_1"] = df.apply(
        lambda x: surebet_profit(x["more_x"], x["less_y"]), axis=1
    )
    df["profit_2"] = df.apply(
        lambda x: surebet_profit(x["less_x"], x["more_y"]), axis=1
    )

    df = pd.concat([df.loc[df["surebet_1"]], df.loc[df["surebet_2"]]])
    df["profit"] = df[["profit_1", "profit_2"]].max(axis=1)
    df = df.sort_values("profit", ascending=False)
    return df


# we generate the message with the info we are going to send to telegram
def generate_message(df: pd.DataFrame) -> str:
    df["text"] = df.apply(
        lambda x: f"Market: {x['market']}\nTeam: {x['team_x']}\nPlayer: {x['player']}\Line: {x['line']}\nChúntala (more): {x['more_x']}\nBetano (less): {x['less_y']}\nProfit: {round(x['profit']*100, 2)}%"
        if x["surebet_1"]
        else f"Market: {x['market']}\nTeam: {x['team_x']}\Player: {x['player']}\nLine: {x['line']}\nChúntala (less): {x['less_x']}\nBetano (more): {x['more_y']}\nProfit: {round(x['profit']*100, 2)}%",
        axis=1,
    )
    return df
