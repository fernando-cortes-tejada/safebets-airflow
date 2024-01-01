import time
from datetime import datetime

from .. import utils as sb_utils
from . import utils as bt_utils
from ...utils import send_message

from .entities import INFO


def scrape(**kwargs):
    league = kwargs["league"]
    category = kwargs["category"]
    timeout = kwargs["timeout"]

    # get the current datetime
    dt_ini = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # initialize the flags for scraping
    flag_betano = True
    i = 0
    while flag_betano:
        try:
            # call the scraping function
            df_betano = scrape_(league, category, dt_ini, timeout)
        except ValueError as e:
            # inform if the scraping failed
            send_message(f"Betano ({league.upper()}:{category}) failed")
            print(str(e))
        else:
            if len(df_betano) > 0:
                send_message(
                    f"Betano ({league.upper()}:{category}) OK - {len(df_betano)} records"
                )
                flag_betano = False
            if i > 0:
                send_message(f"Betano ({league.upper()}:{category}) - 0 records")
                flag_betano = False
            i += 1
    df_betano.to_csv(f"src/data/scraped_df/betano_{league}_{category}.csv", index=False)
    print(
        f'The file "src/data/scraped_df/betano_{league}_{category}.csv" was written with {len(df_betano)} records'
    )


# betano scraping function
def scrape_(league: str, category: str, dt_ini: str, timeout: int):
    # initialize the variables
    i = 0

    # get the url to scrape
    url = INFO.get(league).get("url")

    # get the table number (minimum and maximum) to scrape
    num_table_min = INFO.get(league).get("category").get(category).get("num_table_min")
    num_table_max = INFO.get(league).get("category").get(category).get("num_table_max")

    # get the markets to scrape
    markets = INFO.get(league).get("category").get(category).get("markets")

    # we will just try to scrape twice
    while i < 2:
        i += 1
        info = []

        # prod=True means that the browser will be headless
        # we initialize the driver with sleep=2 for the page to load
        driver = sb_utils.initiate_driver(prod=True)
        sb_utils.open_browser(driver, url, 2)

        # we check if the time is over (to not overload the server)
        if bt_utils.check_time(dt_ini, timeout, driver):
            return bt_utils.return_info(info)

        # sometimes betano shows a popup, we close it
        bt_utils.close_button(driver)

        # we get the games
        games = bt_utils.get_games(driver)
        if not games:
            continue

        # iterate over the games
        for j in range(len(games)):
            if bt_utils.check_time(dt_ini, timeout, driver):
                return bt_utils.return_info(info)

            # we open the game and wait for it to load
            driver.get(games[j])
            time.sleep(1)

            print(f"Betano: game {j+1} of {len(games)}")

            # we click the players section
            click_players_bool = bt_utils.click_players_button(driver)
            if not click_players_bool:
                continue

            # we get the total table of plays
            total_table = bt_utils.get_total_table(driver)
            if total_table is None:
                continue

            # we get the table of markets
            markets_table = bt_utils.get_markets_table(total_table)
            if not markets_table:
                continue

            # we iterate over the markets that correspond to the category
            for k in range(num_table_min - 1, min(len(markets_table), num_table_max)):
                if bt_utils.check_time(dt_ini, timeout, driver):
                    return bt_utils.return_info(info)

                print(f"Betano: market {k+1} de {len(markets_table)}")
                market = bt_utils.get_mercado(markets_table[k])
                if market is None:
                    continue

                # we validate if the market is in the markets list of the category
                if market in markets:
                    # we show all the plays
                    bt_utils.click_show_everything(markets_table[k])

                    # we get each team table
                    teams_table = bt_utils.get_teams_table(markets_table[k])
                    if teams_table is None:
                        continue

                    # we iterate over the teams
                    for l in range(len(teams_table)):
                        if bt_utils.check_time(dt_ini, timeout, driver):
                            return bt_utils.return_info(info)

                        # we get the information related to the team
                        print(f"Betano: team {l+1} of {len(teams_table)}")
                        team = bt_utils.get_team_name(teams_table[l])

                        # if we got the team information, we get the plays information
                        if team:
                            rows = bt_utils.get_rows(teams_table[l])
                            for m in range(len(rows)):
                                info += [bt_utils.get_info(rows[m], team, market)]
                    break

        # if we got information, we return it
        if info:
            driver.close()
            return bt_utils.return_info(info)
