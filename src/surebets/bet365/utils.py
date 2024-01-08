from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
import pandas as pd
import re
import math
from datetime import datetime

from src.surebets.entities import DICT_NBA_TEAMS, DICT_BETANO_CHUNTALA, DF_COLS


def get_game_list(driver: webdriver.Chrome) -> WebElement | None:
    try:
        game_list = driver.find_element(
            by=By.CLASS_NAME, value="market-table.ng-star-inserted"
        )
    except:
        print("Te Apuesto: game list not found")
        driver.close()
        return None
    else:
        print("game list ok")
        return game_list


def get_days(game_list: webdriver.Chrome) -> list | None:
    try:
        days = game_list.find_elements(
            by=By.XPATH,
            value="//*[starts-with(@class, 'group-events-table')]",
        )
    except:
        print("Te Apuesto: days not found")
        game_list.close()
        return None
    else:
        print(f"Chuntala: {len(days)} days found")
        return days


def get_games(days: list) -> list | None:
    try:
        for day in days:
            if "games" in locals():
                games += day.find_elements(
                    by=By.XPATH, value="//tr[starts-with(@class, 'ng-tns')]"
                )
            else:
                games = day.find_elements(
                    by=By.XPATH, value="//tr[starts-with(@class, 'ng-tns')]"
                )
    except:
        print("Te Apuesto: games not found")
        return None
    else:
        print(f"Chuntala: {len(games)} games found")
        return games


def click_game(driver: webdriver.Chrome, time_sleep: int = 1) -> bool:
    try:
        driver.click()
    except:
        print("Chuntala: game not found")
        return False
    else:
        time.sleep(time_sleep)
        print("Chuntala: game ok")
        return True


def get_carousels(driver: webdriver.Chrome) -> list | None:
    try:
        carousels = driver.find_element(
            by=By.CLASS_NAME, value="style__Menu-sc-c63ugu-2.liWuKt.betsMenu__filter"
        ).find_elements(by=By.CLASS_NAME, value="betsMenu__menu-item")
    except:
        print("Chuntala: carousels not found")
        return None
    else:
        print(f"Chuntala: {len(carousels)} carousels found")
        return carousels


def click_carousel(carrusel: webdriver.Chrome, time_sleep: int = 1) -> bool:
    try:
        carrusel.click()
        print(f"Chuntala: carousel {carrusel.text} ok")
    except Exception as e:
        print(e)
        print("Chuntala: carousel not found")
        return False
    else:
        time.sleep(time_sleep)
        return True


def get_markets_table(driver: webdriver.Chrome) -> webdriver.Chrome:
    try:
        tabla_mercados = driver.find_element(
            by=By.CLASS_NAME,
            value="infinite-scroll-component ",
        )
    except:
        print("Chuntala: markets table not found")
        return False
    else:
        print("Chuntala: markets table ok")
        return tabla_mercados


def get_plays(driver: webdriver.Chrome) -> tuple:
    try:
        plays = driver.find_elements(
            by=By.CLASS_NAME,
            value="style__Header-sc-s6lgwx-5.hOzuiU.market-collapse",
        )
        odds = driver.find_elements(
            by=By.CLASS_NAME,
            value="style__Body-sc-s6lgwx-6.cIJRCQ.markets__body-container",
        )
    except:
        print("Chuntala: plays not found")
        return None, None
    else:
        print(f"Chuntala: {len(plays)} plays found")
        return plays, odds


def get_player(string: str) -> str:
    return string[0 : (string.find("(") - 1)]


def get_team(string: str) -> str:
    return DICT_NBA_TEAMS.get(
        string[(string.find("(") + 1) : (string.find(")"))],
        string[(string.find("(") + 1) : (string.find(")"))],
    )


def get_market(string: str) -> str:
    return DICT_BETANO_CHUNTALA.get(
        string[(string.find(")") + 2) : (string.find("\n"))],
        string[(string.find(")") + 2) : (string.find("\n"))],
    )


def get_line(string: str) -> float:
    line = string.split("\n")[-4].split(" ")[-1].replace("(", "").replace(")", "")
    return float(line)


def get_info(string: str) -> dict:
    info = {
        "player": get_player(string),
        "team": get_team(string),
        "market": get_market(string),
        "line": get_line(string),
        "more": float(string.split("\n")[-3]),
        "less": float(string.split("\n")[-1]),
    }
    return info


def get_alt_info(string: str) -> list:
    info = []
    for l in range(int((len(string.split("\n")) - 1) / 2)):
        player = string.split("\n")[(2 * l) + 1]
        team = ""
        market = DICT_BETANO_CHUNTALA.get(
            string.split("\n")[0].split(" ")[-1],
            string.split("\n")[0].split(" ")[-1],
        )
        line = float(re.findall(r"\b\d+\b", string.split("\n")[0])[0]) - 0.5
        more = float(string.split("\n")[(2 * l) + 2])
        less = math.nan

        dict_ = {
            "website": "CHUNTALA",
            "market": market,
            "team": team,
            "player": player,
            "line": line,
            "more": more,
            "less": less,
        }
        info += [dict_]
    return info


def get_linea_mlb(string: str, mercado: str) -> float:
    if mercado == "Jonrones":
        linea = 0.5
    else:
        valor = re.findall(r"\d+", string.split("\n")[0])
        if valor:
            linea = float(valor[0]) - 0.5
        else:
            linea = 0.5
    return float(linea)


def get_mlb_info(string: str) -> list:
    info = []
    for m in range(int((len(string.split("\n")) - 1) / 2)):
        player = string.split("\n")[(2 * m) + 1]
        team = ""
        market = DICT_BETANO_CHUNTALA.get(string.split("\n")[0])
        line = get_linea_mlb(string, market)
        more = float(string.split("\n")[(2 * m) + 2])
        less = math.nan

        dict_ = {
            "website": "CHUNTALA",
            "market": market,
            "team": team,
            "player": player,
            "line": line,
            "more": more,
            "less": less,
        }
        info += [dict_]
    return info


def check_time(dt_ini: str, timeout: int, driver: webdriver.Chrome) -> bool:
    dt_fin = datetime.now()
    if (dt_fin - datetime.strptime(dt_ini, "%Y-%m-%d %H:%M:%S")).seconds > timeout:
        print("Chuntala: timeout")
        driver.close()
        return True
    else:
        return False


def return_info(info: list) -> pd.DataFrame:
    if info:
        return pd.DataFrame.from_dict(info)
    else:
        return pd.DataFrame(columns=DF_COLS)


def get_plays_str(play, odd) -> str | None:
    try:
        string = play.text + "\n" + odd.text
    except:
        string = None
        print("Chuntala: play string not found")
    return string
