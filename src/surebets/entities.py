CHROMEDRIVER_PATH = "src/execs/chromedriver_linux64/chromedriver"
LIST_JUGADORES = [
    "Jugadores",
    "Jugadores primer cuarto",
    "Rebotes del jugador",
    "Asistencias del jugador",
    "Robos de balón del jugador",
    "Pérdidas de balón del jugador",
    "Bloqueos del jugador",
    "Puntos y rebotes del jugador",
    "Puntos y asistencias del jugador",
    "Asistencias y rebotes del jugador",
    "Pts, asis y reb del jugador",
    "Triples anotados del jugador",
    # "Especiales del jugador",
]
# how each market is called in betano:chuntala as k:v pairs
DICT_BETANO_CHUNTALA = {
    "total de puntos": "Puntos Más/Menos",
    "Points": "Puntos Más/Menos",
    "puntos": "Puntos Más/Menos",
    "Puntos": "Puntos Más/Menos",
    "Rebounds": "Rebotes Más/Menos",
    "total de rebotes": "Rebotes Más/Menos",
    "Rebotes": "Rebotes Más/Menos",
    "rebotes": "Rebotes Más/Menos",
    "Assists": "Asistencias Más/Menos",
    "total de asistencias": "Asistencias Más/Menos",
    "asistencias": "Asistencias Más/Menos",
    "Asistencias": "Asistencias Más/Menos",
    "total de pérdidas de balón": "Pérdidas de balón Más/Menos",
    "Pérdidas de balón": "Pérdidas de balón Más/Menos",
    "Turnovers": "Pérdidas de balón Más/Menos",
    "Points and Rebounds": "Puntos+Rebotes Más/Menos",
    "puntos y rebotes": "Puntos+Rebotes Más/Menos",
    "puntos y asistencias": "Puntos+Asistencias Más/Menos",
    "Points and Assists": "Puntos+Asistencias Más/Menos",
    "Assists and Rebounds": "Rebotes+Asistencias Más/Menos",
    "asistencias y rebotes": "Rebotes+Asistencias Más/Menos",
    "Asistencias y Rebotes": "Rebotes+Asistencias Más/Menos",
    "Points, Assists and Rebounds": "Puntos+Rebotes+Asistencias Más/Menos",
    "puntos, asistencias y rebotes": "Puntos+Rebotes+Asistencias Más/Menos",
    "total de triples anotados": "Total de Tiros de tres puntos anotados Más/Menos",
    "de triples anotados": "Total de Tiros de tres puntos anotados Más/Menos",
    "Three-Point Made": "Total de Tiros de tres puntos anotados Más/Menos",
    "triples": "Total de Tiros de tres puntos anotados Más/Menos",
    "puntos en el primer cuarto": "Puntos 1er Periodo",
    "1st Quarter Rebounds": "Rebotes 1er Periodo",
    "1st Quarter Points": "Puntos 1er Periodo",
    "Rebotes en el primer cuarto": "Rebotes 1er Periodo",
    "1st Quarter Rebounds": "Rebotes 1er Periodo",
    "1st Quarter Assists": "Asistencias 1er Periodo",
    "Asistencias en el primer cuarto": "Asistencias 1er Periodo",
    "Steals": "Robos Más/Menos",
    "Blocks": "Bloqueos Más/Menos",
    "Jonrón en cualquier momento": "Jonrones",
    "Player To Record a Run": "Carreras",
    "Player To Record 2 or More Runs": "Carreras",
    "Jugador registra 3 o más carreras": "Carreras",
    "Jugador registra 4 o más carreras": "Carreras",
    "Player To Record a Hit": "Hits",
    "Player To Record 2 or More Hits": "Hits",
    "Player To Record 3 or More Hits": "Hits",
    "Player To Record 4 or More Hits": "Hits",
    "Player To Record an RBI": "RBI del Bateador",
    "Player To Record 2 or More RBI's": "RBI del Bateador",
    "Player To Record 3 or More RBI's": "RBI del Bateador",
}
# how each team is called in betano:chuntala as k:v pairs
DICT_NBA_TEAMS = {
    "ATL Hawks": "Atlanta Hawks",
    "BKN Nets": "Brooklyn Nets",
    "BOS Celtics": "Boston Celtics",
    "CHA Hornets": "Charlotte Hornets",
    "CHI Bulls": "Chicago Bulls",
    "CLE Cavaliers": "Cleveland Cavaliers",
    "DAL Mavericks": "Dallas Mavericks",
    "DEN Nuggets": "Denver Nuggets",
    "DET Pistons": "Detroit Pistons",
    "GSW Warriors": "Golden State Warriors",
    "GS Warriors": "Golden State Warriors",
    "HOU Rockets": "Houston Rockets",
    "IND Pacers": "Indiana Pacers",
    "LAC Clippers": "Los Angeles Clippers",
    "LA Clippers": "Los Angeles Clippers",
    "LAL Lakers": "Los Angeles Lakers",
    "LA Lakers": "Los Angeles Lakers",
    "MEM Grizzlies": "Memphis Grizzlies",
    "MIA Heat": "Miami Heat",
    "MIL Bucks": "Milwaukee Bucks",
    "MIN Timberwolves": "Minnesota Timberwolves",
    "NOP Pelicans": "New Orleans Pelicans",
    "NO Pelicans": "New Orleans Pelicans",
    "NYK Knicks": "New York Knicks",
    "NY Knicks": "New York Knicks",
    "OKC Thunder": "Oklahoma City Thunder",
    "ORL Magic": "Orlando Magic",
    "PHI 76ers": "Philadelphia 76ers",
    "PHX Suns": "Phoenix Suns",
    "POR Trail Blazers": "Portland Trail Blazers",
    "SAC Kings": "Sacramento Kings",
    "SAC KIngs": "Sacramento Kings",
    "SAS Spurs": "San Antonio Spurs",
    "SA Spurs": "San Antonio Spurs",
    "TOR Raptors": "Toronto Raptors",
    "UTA Jazz": "Utah Jazz",
    "WAS Wizards": "Washington Wizards",
}
DF_COLS = ["website", "market", "team", "player", "line", "more", "less"]
