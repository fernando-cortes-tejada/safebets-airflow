import pandas as pd
from datetime import datetime
from src.surebets import utils as sb_utils
from src.surebets.teapuesto import utils as ta_utils
from src.utils import send_message

from src.surebets.teapuesto.entities import INFO, NOT_PLAYERS


# teapuesto scraping function
def scrape(league: str, category: str, dt_ini: str, timeout: int) -> pd.DataFrame:
    # initialize the variables
    i = 0
    league = "nba"

    # get the url to scrape
    url = INFO.get(league).get("url")

    # get the number of the carrusel to scrape
    # num_carousel = INFO.get(league).get("category").get(category).get("num_carousel")

    # get the name of the carrusel to scrape
    # name_carousel = INFO.get(league).get("category").get(category).get("name_carousel")

    # if the league is mlb, get the name of the play to scrape
    # if league == "mlb":
    #    name_play = INFO.get(league).get("category").get(category).get("name_play")

    # we will just try to scrape the data twice
    while i < 2:
        i += 1
        info = []

        # prod = True means that the browser will be headless
        # we initialize the driver with time sleep of 10 seconds to wait for the page to load

        url = "https://www.pinnacle.com/es/basketball/nba/matchups"
        driver = sb_utils.initiate_driver(prod=False)
        sb_utils.open_browser(driver, url, 10)

        driver.quit()

        # we check if the time is over (to not overload the server)
        # if ta_utils.check_time(dt_ini, timeout, driver):
        #    return ta_utils.return_info(info)

        # we get the list of the matches (separated by days)
        game_list = ta_utils.get_game_list(driver)
        if game_list is None:
            continue

        # we get the days of the matches
        days = ta_utils.get_days(game_list)
        if days is None:
            continue

        # get the list of the matches
        games = ta_utils.get_games(days)
        if games is None:
            driver.close()
            continue

        # we start iterating over the matches
        for j in range(0, len(games)):
            if ta_utils.check_time(dt_ini, timeout, driver):
                return ta_utils.return_info(info)

            # click on the match
            print(f"Te Apuesto: Partido {j+1} de {len(games)}")
            click_game_bool = ta_utils.click_game(games[j], 10)

            # if the click on the match opened it, continue the scraping
            if click_game_bool:
                carousels = ta_utils.get_carousels(driver)
                if not carousels:
                    continue

                    # we iterate over the carousels
                    # for k in range(num_carousel, len(carousels)):
                    if ta_utils.check_time(dt_ini, timeout, driver):
                        return ta_utils.return_info(info)

                    if carousels[k].text == name_carousel:
                        # click the carousel with the name of the category
                        if category == "puntos":
                            click_carousel_bool = ta_utils.click_carousel(
                                carousels[k + 1]
                            )
                        elif league == "mlb":
                            click_carousel_bool = ta_utils.click_carousel(
                                carousels[k + 2]
                            )
                        click_carousel_bool = ta_utils.click_carousel(carousels[k])
                        if not click_carousel_bool:
                            driver.close()
                            break

                        # get the plays and the odds
                        plays, odds = ta_utils.get_plays(driver)
                        if plays is None:
                            break

                        # we iterate over the plays
                        for l in range(len(plays)):
                            if ta_utils.check_time(dt_ini, timeout, driver):
                                return ta_utils.return_info(info)

                            print(f"Te Apuesto: play {l+1} of {len(plays)}")

                            strings = ta_utils.get_plays_str(plays[l], odds[l])
                            if league == "nba":
                                # we do some validations depending on the type of play
                                if not strings:
                                    continue
                                if strings.count("\n") == 3:
                                    continue

                                if (strings.count("\n") == 8) & (
                                    strings.split(" ")[0] not in NOT_PLAYERS
                                ):
                                    strings = [
                                        "\n".join(
                                            strings.split("\n")[0:3]
                                            + strings.split("\n")[5:7]
                                        ),
                                        "\n".join(
                                            [strings.split("\n")[0]]
                                            + strings.split("\n")[3:5]
                                            + strings.split("\n")[7:9]
                                        ),
                                    ]
                                else:
                                    strings = [strings]

                                for string in strings:
                                    if string.split(" ")[0] not in NOT_PLAYERS:
                                        try:
                                            info += [
                                                {"website": "TEAPUESTO"}
                                                | ta_utils.get_info(string)
                                            ]
                                        except:
                                            continue
                                    elif string.split(" ")[0] in ["Player", "Jugador"]:
                                        try:
                                            info += ta_utils.get_alt_info(string)
                                        except:
                                            continue
                            elif league == "mlb":
                                if strings.split("\n")[0] in name_play:
                                    info += ta_utils.get_mlb_info(strings)
                        break

        # if the scraping was successful, we return the info and close the driver
        if info:
            driver.close()
            return ta_utils.return_info(info)
