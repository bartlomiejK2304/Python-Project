import requests
import pandas as pd

def pobierz_dane():
    """
    Pobranie danych giełdowych BTC z API (z obsługą błędów)
    """
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100"
    odpowiedz = requests.get(url)
    
    if odpowiedz.status_code != 200:
        raise Exception(f"Błąd API: {odpowiedz.status_code}")
    
    return odpowiedz.json()


def moj_generator(dane):
    """
    Generator zwracający kolejne elementy
    """
    for element in dane:
        yield element


def czy_jest_obrot(wiersz):
    """
    Sprawdza czy wolumen > 0
    """
    return float(wiersz[5]) > 0


def zrob_slownik(wiersz):
    """
    Zamiana listy z API na słownik
    """
    return {
        'data': pd.to_datetime(wiersz[0], unit='ms'),
        'otwarcie': float(wiersz[1]),
        'zamkniecie': float(wiersz[4]),
        'wolumen': float(wiersz[5])
    }


def suma_wolumenow(lista):
    """
    Suma wolumenów (wydajniej niż rekurencja)
    """
    return sum(lista)


def grupuj_pandas(df):
    """
    Grupowanie danych (dni tygodnia po polsku)
    """
    df = df.copy()

    dni_map = {
        'Monday': 'Poniedziałek',
        'Tuesday': 'Wtorek',
        'Wednesday': 'Środa',
        'Thursday': 'Czwartek',
        'Friday': 'Piątek',
        'Saturday': 'Sobota',
        'Sunday': 'Niedziela'
    }

    df['dzien'] = df['data'].dt.day_name().map(dni_map)

    wynik = df.groupby('dzien')['wolumen'].mean().reset_index()

    kolejnosc = [
        'Poniedziałek', 'Wtorek', 'Środa',
        'Czwartek', 'Piątek', 'Sobota', 'Niedziela'
    ]

    wynik['dzien'] = pd.Categorical(wynik['dzien'], categories=kolejnosc, ordered=True)
    wynik = wynik.sort_values('dzien')

    return wynik


def oblicz_mediane(df, kolumna):
    return df[kolumna].median()


def oblicz_odchylenie(df, kolumna):
    return df[kolumna].std()