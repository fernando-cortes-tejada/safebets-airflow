import pandas as pd
from datetime import datetime
from .. import utils as sb_utils
from . import utils as ch_utils
from ...utils import send_message

from .entities import INFO, NOT_PLAYERS


def scrape(**kwargs) -> None:
    league = kwargs["league"]
    category = kwargs["category"]
    timeout = kwargs["timeout"]

    # get the current datetime
    dt_ini = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # initialize the flags for scraping
    flag_chuntala = True
    i = 0
    while flag_chuntala:
        try:
            # call the scraping function
            df_chuntala = scrape_(league, category, dt_ini, timeout)
        except ValueError as e:
            # inform if the scraping failed
            send_message(f"Chuntala ({league.upper()}:{category}) failed")
            print(str(e))
        else:
            try:
                if len(df_chuntala) > 0:
                    send_message(
                        f"Chúntala ({league.upper()}:{category}) OK - {len(df_chuntala)} records"
                    )
                    flag_chuntala = False
                elif i > 0:
                    send_message(f"Chúntala ({league.upper()}:{category}) - 0 records")
                    flag_chuntala = False
                df_chuntala.to_csv(
                    f"src/data/scraped_df/chuntala_{league}_{category}.csv", index=False
                )
                print(
                    f'The file "src/data/scraped_df/chuntala_{league}_{category}.csv" was written with {len(df_chuntala)} records'
                )
            except ValueError as e:
                print(str(e))
            i += 1


# chuntala scraping function
def scrape_(league: str, category: str, dt_ini: str, timeout: int) -> pd.DataFrame:
    # initialize the variables
    i = 0

    # get the url to scrape
    url = INFO.get(league).get("url")

    # get the number of the carrusel to scrape
    num_carousel = INFO.get(league).get("category").get(category).get("num_carousel")

    # get the name of the carrusel to scrape
    name_carousel = INFO.get(league).get("category").get(category).get("name_carousel")

    # if the league is mlb, get the name of the play to scrape
    if league == "mlb":
        name_play = INFO.get(league).get("category").get(category).get("name_play")

    # we will just try to scrape the data twice
    while i < 2:
        i += 1
        info = []

        # prod = True means that the browser will be headless
        # we initialize the driver with time sleep of 10 seconds to wait for the page to load
        driver = sb_utils.initiate_driver(prod=True)
        sb_utils.open_browser(driver, url, 10)

        # we check if the time is over (to not overload the server)
        if ch_utils.check_time(dt_ini, timeout, driver):
            return ch_utils.return_info(info)

        # we get the list of the matches (separated by days)
        game_list = ch_utils.get_game_list(driver)
        if game_list is None:
            continue

        # we get the days of the matches
        days = ch_utils.get_days(game_list)
        if days is None:
            continue

        # get the list of the matches
        games = ch_utils.get_games(days)
        if games is None:
            driver.close()
            continue

        # we start iterating over the matches
        for j in range(0, len(games)):
            if ch_utils.check_time(dt_ini, timeout, driver):
                return ch_utils.return_info(info)

            # click on the match
            print(f"Chuntala: Partido {j+1} de {len(games)}")
            click_game_bool = ch_utils.click_game(games[j], 10)

            # if the click on the match opened it, continue the scraping
            if click_game_bool:
                carousels = ch_utils.get_carousels(driver)
                if not carousels:
                    continue

                # we iterate over the carousels
                for k in range(num_carousel, len(carousels)):
                    if ch_utils.check_time(dt_ini, timeout, driver):
                        return ch_utils.return_info(info)

                    if carousels[k].text == name_carousel:
                        # click the carousel with the name of the category
                        if category == "puntos":
                            click_carousel_bool = ch_utils.click_carousel(
                                carousels[k + 1]
                            )
                        elif league == "mlb":
                            click_carousel_bool = ch_utils.click_carousel(
                                carousels[k + 2]
                            )
                        click_carousel_bool = ch_utils.click_carousel(carousels[k])
                        if not click_carousel_bool:
                            driver.close()
                            break

                        # get the plays and the odds
                        plays, odds = ch_utils.get_plays(driver)
                        if plays is None:
                            break

                        # we iterate over the plays
                        for l in range(len(plays)):
                            if ch_utils.check_time(dt_ini, timeout, driver):
                                return ch_utils.return_info(info)

                            print(f"Chuntala: play {l+1} of {len(plays)}")

                            strings = ch_utils.get_plays_str(plays[l], odds[l])
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
                                                {"website": "CHUNTALA"}
                                                | ch_utils.get_info(string)
                                            ]
                                        except:
                                            continue
                                    elif string.split(" ")[0] in ["Player", "Jugador"]:
                                        try:
                                            info += ch_utils.get_alt_info(string)
                                        except:
                                            continue
                            elif league == "mlb":
                                if strings.split("\n")[0] in name_play:
                                    info += ch_utils.get_mlb_info(strings)
                        break

        # if the scraping was successful, we return the info and close the driver
        if info:
            driver.close()
            return ch_utils.return_info(info)
