NBA_URL = (
    # "https://www.teapuesto.pe/sport/odds?timeFrame=all&tournaments=193912&type=matches"
    "https://www.bet365.com/#/AC/B18/C20604387/D19/E18728752/F19/"
)
MLB_URL = "https://www.chuntalaya.pe/classic-sports/match/Baseball/North%20America/608"
NOT_PLAYERS = ["Jugador", "Player", "Primera", "Máximo"]
NBA_CATEGORY_INFO = {
    "triples": {"num_carousel": 3, "name_carousel": "Triples anotados del jugador"},
    "bloqueos": {"num_carousel": 3, "name_carousel": "Bloqueos del jugador"},
    "perdidas": {"num_carousel": 3, "name_carousel": "Pérdidas de balón del jugador"},
    "robos": {"num_carousel": 3, "name_carousel": "Robos de balón del jugador"},
    "asistencias": {"num_carousel": 3, "name_carousel": "Asistencias del jugador"},
    "rebotes": {"num_carousel": 3, "name_carousel": "Rebotes del jugador"},
    "primer_cuarto": {"num_carousel": 2, "name_carousel": "Jugadores primer cuarto"},
    "puntos": {"num_carousel": 2, "name_carousel": "Jugadores"},
}
MLB_CATEGORY_INFO = {
    "jonrones": {
        "num_carousel": 4,
        "name_carousel": "Jugadores",
        "name_play": ["Jonrón en cualquier momento"],
    },
    "carreras": {
        "num_carousel": 4,
        "name_carousel": "Jugadores",
        "name_play": [
            "Player To Record a Run",
            "Player To Record 2 or More Runs",
            "Jugador registra 3 o más carreras",
            "Jugador registra 4 o más carreras",
        ],
    },
    "hits": {
        "num_carousel": 4,
        "name_carousel": "Jugadores",
        "name_play": [
            "Player To Record a Hit",
            "Player To Record 2 or More Hits",
            "Player To Record 3 or More Hits",
            "Player To Record 4 or More Hits",
        ],
    },
    "rbi": {
        "num_carousel": 4,
        "name_carousel": "Jugadores",
        "name_play": [
            "Player To Record an RBI",
            "Player To Record 2 or More RBI's",
            "Player To Record 3 or More RBI's",
        ],
    },
}
INFO = {
    "nba": {"url": NBA_URL, "category": NBA_CATEGORY_INFO},
    "mlb": {"url": MLB_URL, "category": MLB_CATEGORY_INFO},
}
