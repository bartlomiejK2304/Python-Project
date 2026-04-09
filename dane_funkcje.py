import requests
import pandas as pd

def pobierz_dane():
    """
    Pobranie danych gieldowych btc z api
    """
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100"
    odpowiedz = requests.get(url)
    return odpowiedz.json()

def moj_generator(dane):
    """
    Zwraca po jednym elemencie z listy
    """
    for element in dane:
        yield element

def czy_jest_obrot(wiersz):
    """
    Sprawdza czy wolumen jest wiekszy niz zero
    """
    return float(wiersz[5]) > 0

def zrob_slownik(wiersz):
    """
    Zamienia liste z api na slownik
    """
    return {
        'data': pd.to_datetime(wiersz[0], unit='ms'),
        'otwarcie': float(wiersz[1]),
        'zamkniecie': float(wiersz[4]),
        'wolumen': float(wiersz[5])
    }

def suma_rekurencyjna(lista):
    """
    Rekurencyjne dodawanie elementow listy
    """
    if len(lista) == 0:
        return 0
    return lista[0] + suma_rekurencyjna(lista[1:])

def grupuj_pandas(df):
    """
    Split apply combine w bibliotece pandas
    """
    df['dzien'] = df['data'].dt.day_name()
    wynik = df.groupby('dzien')['wolumen'].mean().reset_index()
    return wynik