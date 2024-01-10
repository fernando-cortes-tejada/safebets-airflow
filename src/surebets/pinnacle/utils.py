from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
import pandas as pd
import re
import math
from datetime import datetime

from src.surebets.entities import DICT_NBA_TEAMS, DICT_BETANO_CHUNTALA


# get the list of games (not live games)
def get_game_list(driver: webdriver.Chrome, timeout: int = 20) -> WebElement | None:
    t1 = datetime.now()
    t2 = datetime.now()
    while (t2 - t1).seconds < timeout:
        t2 = datetime.now()
        try:
            game_list = driver.find_element(
                by=By.CLASS_NAME, value="contentBlock.square"
            )
        except:
            pass
        else:
            print("game list ok")
            return game_list

    print("game list not found")
    return None


def get_games_url(game_list: webdriver.Chrome) -> list:
    games = game_list.find_elements(
        by=By.XPATH, value="//a[starts-with(@href, '/es/basketball/nba')]"
    )
    game_urls = []
    if games:
        for game in games:
            game_urls += [game.get_attribute("href")]
        game_urls = list(set(game_urls))

    return game_urls


def get_live_games(driver: webdriver.Chrome, timeout: int = 1) -> list:
    live_games_url = []
    t1 = datetime.now()
    t2 = datetime.now()
    while (t2 - t1).seconds < timeout:
        t2 = datetime.now()
        try:
            live_games = driver.find_element(
                by=By.XPATH, value="//div[@data-test-id='LiveContainer']"
            )
            live_games = live_games.find_elements(
                by=By.CLASS_NAME, value="style_metadata__3MrIC"
            )
            len(live_games)
            for live_game in live_games:
                live_games_url.append(
                    live_game.find_element(by=By.XPATH, value="*")
                    .find_element(by=By.XPATH, value="*")
                    .get_attribute("href")
                )
        except:
            pass
        else:
            print("live game list ok")
            return live_games_url

    return live_games_url


def check_live_game(driver: webdriver.Chrome, timeout: int = 5) -> bool:
    t1 = datetime.now()
    t2 = datetime.now()
    while (t2 - t1).seconds < timeout:
        t2 = datetime.now()
        try:
            live = driver.find_element(
                by=By.CLASS_NAME, value="style_liveStatus__2pXfr"
            )
        except:
            pass
        else:
            return live.text == "EN VIVO"

    return False


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


def get_carousels(driver: webdriver.Chrome, timeout: int = 20) -> list:
    t1 = datetime.now()
    t2 = datetime.now()
    while (t2 - t1).seconds < timeout:
        t2 = datetime.now()
        try:
            carousel = driver.find_element(
                by=By.CLASS_NAME, value="style_filterBarContent__1Oe4N"
            )
            carousels = carousel.find_elements(
                by=By.CLASS_NAME, value="style_button__3zn2w"
            )
        except:
            pass
        else:
            print("carousels ok")
            return carousels
    return []


def get_markets_table(driver: webdriver.Chrome, timeout: int = 20) -> webdriver.Chrome:
    t1 = datetime.now()
    t2 = datetime.now()
    while (t2 - t1).seconds < timeout:
        t2 = datetime.now()
        try:
            markets_table = driver.find_elements(
                by=By.CLASS_NAME,
                value="style_primary__uMCOh.style_marketGroup__rIPR4",
            )
        except:
            pass
        else:
            print("markets table ok")
            return markets_table
    return []


def more_info(market_: webdriver.Chrome) -> None:
    market_.find_element(by=By.CLASS_NAME, value="style_toggleMarkets__2IYz8").click()


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


def get_plays_str(play, odd) -> str | None:
    try:
        string = play.text + "\n" + odd.text
    except:
        string = None
        print("Chuntala: play string not found")
    return string


def data_winner(game_name: str, market: str, string: list) -> list:
    info = []
    for i in range(2):
        data_ = string[2:][(i * 2) : (i * 2 + 2)]
        info += [
            {
                "website": "pinnacle",
                "game": game_name,
                "market": market,
                "team": data_[0],
                "more": data_[1],
            }
        ]
    return info


def data_handicap(game_name: str, teams: list, market: str, string: list) -> list:
    info = []
    for i in range(int((len(string) - 2) / 4)):
        data_ = string[1:][(i * 4 + 1) : ((i + 1) * 4 + 1)]
        info += [
            {
                "website": "pinnacle",
                "game": game_name,
                "market": market,
                "team": teams[0],
                "line": float(data_[0]),
                "more": float(data_[1]),
                "less": float(data_[3]),
            }
        ]
    return info


def data_total(game_name: str, market: str, string: list) -> list:
    info = []
    for i in range(int((len(string) - 1) / 4)):
        data_ = string[(i * 4 + 1) : ((i + 1) * 4 + 1)]
        info += [
            {
                "website": "pinnacle",
                "game": game_name,
                "market": market,
                "line": float(data_[0].split(" ")[-1]),
                "more": float(data_[1]),
                "less": float(data_[3]),
            }
        ]
    return info


def data_total_team(game_name: str, teams: list, market: str, string: list) -> list:
    info = []
    for i in range(2):
        data_ = string[1:][(i * 4 + 1) : ((i + 1) * 4 + 1)]
        info += [
            {
                "website": "pinnacle",
                "game": game_name,
                "market": market,
                "team": teams[i],
                "line": float(data_[0].split(" ")[-1]),
                "more": float(data_[1]),
                "less": float(data_[3]),
            }
        ]
    return info


def data_players(game_name: str, market: str, string: list) -> list:
    info = []
    market = string[0][string[0].find("(") :][1:-1]
    player = string[0][: string[0].find("(") - 1]
    line = [float(s) for s in string[1].split() if s.replace(".", "").isdigit()][0]
    info += [
        {
            "website": "pinnacle",
            "game": game_name,
            "market": market,
            "player": player,
            "line": line,
            "more": float(string[2]),
            "less": float(string[4]),
        }
    ]
    return info
