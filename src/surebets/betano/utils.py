from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
import math
from datetime import datetime
import pandas as pd

from ..entities import DF_COLS


def close_button(driver: webdriver.Chrome, time_sleep: int = 1):
    try:
        closeButton = driver.find_element(
            by=By.XPATH, value='//*[@id="landing-page-modal"]/div/div[1]/button'
        )
    except:
        pass
    else:
        closeButton.click()
        time.sleep(time_sleep)
        print("Betano: close popup ok")


def click_players_button(driver: webdriver.Chrome, time_sleep: int = 1) -> bool:
    try:
        playersButton = driver.find_element(
            by=By.CLASS_NAME,
            value="events-tabs-container__tab__item__button.GTM-1",
        )
    except:
        return False
    else:
        if playersButton.text in ["Especiales de Jugadores", "Jugadores"]:
            playersButton.click()
            time.sleep(time_sleep)
            print("Betano: Especiales de Jugadores button ok")
            return True
        else:
            try:
                playersButton = driver.find_element(
                    by=By.CLASS_NAME,
                    value="events-tabs-container__tab__item__button.GTM-2",
                )
            except:
                return False
            else:
                if playersButton.text in ["Especiales de Jugadores", "Jugadores"]:
                    playersButton.click()
                    time.sleep(time_sleep)
                    print("Betano: Especiales de Jugadores button ok")
                    return True
                else:
                    return False


def get_games(driver: webdriver.Chrome) -> list:
    games_url = []

    try:
        games = driver.find_element(by=By.CLASS_NAME, value="events-list__grid")
        games = games.find_elements(by=By.CLASS_NAME, value="events-list__grid__event")
    except:
        return games_url
    else:
        for game in games:
            games_url += [
                game.find_element(
                    by=By.CLASS_NAME,
                    value="GTM-event-link.events-list__grid__info__main",
                ).get_attribute("href")
            ]
        print(f"Betano: {len(games_url)} games_found")
        return games_url


def get_total_table(driver: webdriver.Chrome) -> WebElement | None:
    try:
        total_table = driver.find_element(by=By.CLASS_NAME, value="markets")
    except:
        return None
    else:
        return total_table


def get_team_name(driver: webdriver.Chrome) -> str:
    try:
        team = driver.find_element(by=By.CLASS_NAME, value="team-header__title").text
    except:
        return ""
    else:
        team = "temp" if team == "" else team
        print(f"Betano: {team}")
        return team


def get_rows(driver: webdriver.Chrome) -> list:
    return driver.find_elements(by=By.CLASS_NAME, value="row")


def abrir_mercados(
    tabla_total: webdriver.Chrome,
    time_sleep: int = 1,
    min_abrir: int = 1,
    max_abrir: int = 16,
):
    try:
        abrirMercados = tabla_total.find_elements(
            by=By.CLASS_NAME, value="sb-arrow.kz-icon-xs.push-right.icon--clickable"
        )
    except:
        return False
    else:
        print(f"Betano: {len(abrirMercados)} mercados encontrados para abrir")
        for i in range(min_abrir - 1, min(len(abrirMercados), max_abrir)):
            if i > 0:
                try:
                    abrirMercados[i].click()
                except:
                    pass
                else:
                    print(f"Betano: Mercado {i} abierto")
        time.sleep(time_sleep)
        return True


def get_jugador(driver: webdriver.Chrome) -> str:
    return driver.find_element(by=By.CLASS_NAME, value="row-title__text").text


def get_linea(driver: webdriver.Chrome, mercado: str) -> float:
    if mercado == "Jonrones":
        return 0.5
    else:
        try:
            linea = float(
                driver.find_element(
                    by=By.CLASS_NAME, value="handicap__single-item"
                ).text
            )
        except:
            linea = math.nan
        return linea


def get_odds(driver: webdriver.Chrome) -> list:
    odds = [
        float(odd)
        for odd in driver.find_element(
            by=By.CLASS_NAME, value="table-selections-wrapper"
        ).text.split("\n")
    ]
    return odds


def get_markets_table(driver: webdriver.Chrome) -> list[WebElement] | None:
    try:
        markets_table = driver.find_elements(
            by=By.CLASS_NAME, value="table-layout-container"
        )
    except:
        return None
    else:
        return markets_table


def get_mercado(driver: webdriver.Chrome) -> str | None:
    try:
        market = driver.find_element(
            by=By.CLASS_NAME, value="table-market-header__text"
        ).text
    except:
        return None
    else:
        print(f"Betano: market {market}")
        return market


def click_show_everything(driver: webdriver.Chrome) -> None:
    try:
        driver.find_element(by=By.CLASS_NAME, value="load-more").click()
    except:
        pass


def get_teams_table(driver: webdriver.Chrome) -> list[WebElement] | None:
    try:
        teams_table = driver.find_elements(by=By.CLASS_NAME, value="team")
    except:
        return None
    else:
        return teams_table


def get_info(row: webdriver.Chrome, equipo: str, mercado: str) -> dict:
    jugador = get_jugador(row)
    linea = get_linea(row, mercado)
    try:
        mas, menos = get_odds(row)
    except:
        mas, menos = math.nan, math.nan
    info = {
        "casa": "BETANO",
        "mercado": mercado,
        "equipo": equipo,
        "jugador": jugador,
        "linea": linea,
        "mas": mas,
        "menos": menos,
    }
    return info


def check_time(dt_ini: str, max_time: int, driver: webdriver.Chrome) -> bool:
    dt_fin = datetime.now()
    if (dt_fin - datetime.strptime(dt_ini, "%Y-%m-%d %H:%M:%S")).seconds > max_time:
        print("Chuntala: Tiempo máximo excedido")
        driver.close()
        return True
    else:
        return False


def return_info(info: list) -> pd.DataFrame:
    if info:
        return pd.DataFrame.from_dict(info)
    else:
        return pd.DataFrame(columns=DF_COLS)
