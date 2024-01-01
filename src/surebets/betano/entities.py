NBA_URL = "https://pe.betano.com/sport/basquetbol/ee-uu/nba/17106r/"
MLB_URL = "https://pe.betano.com/sport/beisbol/ee-uu/mlb/1662/"
NBA_CATEGORY_INFO = {
    "triples": {
        "num_table_min": 4,
        "num_table_max": 4,
        "markets": ["Total de Tiros de tres puntos anotados - Más/Menos"],
    },
    "bloqueos": {
        "num_table_min": 6,
        "num_table_max": 7,
        "markets": ["Bloqueos Más/Menos"],
    },
    "perdidas": {
        "num_table_min": 7,
        "num_table_max": 8,
        "markets": ["Pérdidas de balón Más/Menos"],
    },
    "robos": {
        "num_table_min": 5,
        "num_table_max": 6,
        "markets": ["Robos Más/Menos"],
    },
    "asistencias": {
        "num_table_min": 3,
        "num_table_max": 3,
        "markets": ["Asistencias Más/Menos"],
    },
    "rebotes": {
        "num_table_min": 2,
        "num_table_max": 2,
        "markets": ["Rebotes Más/Menos"],
    },
    "primer_cuarto": {
        "num_table_min": 14,
        "num_table_max": 23,
        "markets": [
            "Puntos 1er Periodo",
            "Rebotes 1er Periodo",
            "Asistencias 1er Periodo",
        ],
    },
    "puntos": {
        "num_table_min": 1,
        "num_table_max": 1,
        "markets": ["Puntos Más/Menos"],
    },
}
MLB_CATEGORY_INFO = {
    "jonrones": {
        "num_table_min": 4,
        "num_table_max": 7,
        "markets": ["Jonrones"],
    },
    "carreras": {"num_table_min": 1, "num_table_max": 3, "markets": ["Carreras"]},
    "hits": {"num_table_min": 7, "num_table_max": 9, "markets": ["Hits"]},
    "rbi": {"num_table_min": 10, "num_table_max": 16, "markets": ["RBI del Bateador"]},
}
INFO = {
    "nba": {"url": NBA_URL, "category": NBA_CATEGORY_INFO},
    "mlb": {"url": MLB_URL, "category": MLB_CATEGORY_INFO},
}
