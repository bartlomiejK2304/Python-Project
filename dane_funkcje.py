import requests
import pandas as pd

def pobierz_dane():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100"
    odpowiedz = requests.get(url)
    
    if odpowiedz.status_code != 200:
        raise Exception(f"Błąd API: {odpowiedz.status_code}")
    
    return odpowiedz.json()


def moj_generator(dane):
    for element in dane:
        yield element


def czy_jest_obrot(wiersz):
    return float(wiersz[5]) > 0


def zrob_slownik(wiersz):
    otwarcie = float(wiersz[1])
    zamkniecie = float(wiersz[4])

    return {
        'data': pd.to_datetime(wiersz[0], unit='ms'),
        'otwarcie': otwarcie,
        'zamkniecie': zamkniecie,
        'wolumen': float(wiersz[5]),
        'zmiana_ceny': zamkniecie - otwarcie
    }


def suma_rekurencyjna(lista):
    if len(lista) == 0:
        return 0
    return lista[0] + suma_rekurencyjna(lista[1:])


def grupuj_pandas(df):
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

    kolejnosc = [
        'Poniedziałek', 'Wtorek', 'Środa',
        'Czwartek', 'Piątek', 'Sobota', 'Niedziela'
    ]

    wynik = df.groupby('dzien')['wolumen'].mean().reset_index()
    wynik['dzien'] = pd.Categorical(wynik['dzien'], categories=kolejnosc, ordered=True)
    wynik = wynik.sort_values('dzien')

    return wynik


def oblicz_mediane(df, kolumna):
    return df[kolumna].median()


def oblicz_odchylenie(df, kolumna):
    return df[kolumna].std()