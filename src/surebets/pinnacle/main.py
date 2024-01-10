import pandas as pd
from datetime import datetime
from src.surebets import utils as sb_utils
from src.surebets.pinnacle import utils as pi_utils

from src.surebets.pinnacle.entities import INFO


#  scraping function
def scrape(league: str, category: str, timeout: int) -> pd.DataFrame:
    t1 = datetime.now()

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
        sb_utils.open_browser(driver, url, 0)

        # we check if the time is over (to not overload the server)
        # if sb_utils.check_time(t1, timeout, driver):
        # return pi_utils.return_info(info)

        # we get the list of the matches (separated by days)
        game_list = pi_utils.get_game_list(driver)
        print(game_list)
        # if game_list is None:
        # continue

        # get the list of the matches
        games = pi_utils.get_games_url(game_list)
        print(games)
        if not games:
            driver.quit()
            continue

        live_games = pi_utils.get_live_games(driver)
        if live_games:
            games = [game for game in games if game not in live_games]

        # we start iterating over the matches
        for game in games:
            print(game)

            if sb_utils.check_time(t1, timeout, driver):
                return sb_utils.return_info(info)

            # we open the game
            driver.get(game)

            game_name = game.split("/")[-3]
            teams = game_name.split("vs")
            teams = [team.replace("-", " ").strip() for team in teams]

            carousels = pi_utils.get_carousels(driver)
            if not carousels:
                continue

            # we iterate over the carousels
            for carousel in carousels:
                if carousel.text == "TODO":
                    continue

                if sb_utils.check_time(t1, timeout, driver):
                    return sb_utils.return_info(info)

                carousel.click()

                markets_table = pi_utils.get_markets_table(driver)

                for market_ in markets_table:
                    string = market_.text.split("\n")
                    if string[-1] == "Más información":
                        pi_utils.more_info(market_)
                        string = market_.text.split("\n")
                        del string[-1]

                    market = string[0]
                    match market:
                        case "Línea de dinero – Partido":
                            market = "winner"
                            info += pi_utils.data_winner(game_name, market, string)
                        case "Hándicap – Partido":
                            market = "handicap"
                            info += pi_utils.data_handicap(
                                game_name, teams, market, string
                            )
                        case "Total – Partido":
                            market = "total"
                            info += pi_utils.data_total(game_name, market, string)
                        case "Total del equipo – Partido":
                            market = "total_team"
                            info += pi_utils.data_total_team(
                                game_name, teams, market, string
                            )
                        case "Línea de dinero – 1.ª parte":
                            market = "winner_first_half"
                            info += pi_utils.data_winner(game_name, market, string)

                    if carousel.text == "PLAYER PROPS":
                        if string[1] == "Ocultar todo":
                            del string[1]
                        info += pi_utils.data_players(game_name, market, string)

        # {
        # "website": "pinnacle",
        # "game": game_name,
        # "market": market,
        # "team": "",
        # "player": "",
        # "line": float(data_[0].split(" ")[-1]),
        # "more": float(data_[1]),
        # "less": float(data_[3]),
        # }

        # if the scraping was successful, we return the info and close the driver
        driver.quit()
        return sb_utils.return_info(info)


t1 = datetime.now()
info = scrape("", "", 100)
(datetime.now() - t1).seconds
