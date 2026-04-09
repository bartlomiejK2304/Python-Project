import requests
import pandas as pd

def pobierz_dane():
    """
    Pobiera surowe dane z API Binance.
    """
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100"
    odpowiedz = requests.get(url)
    
    if odpowiedz.status_code != 200:
        raise Exception(f"Błąd API: {odpowiedz.status_code}")
    
    return odpowiedz.json()

def moj_generator(dane):
    """
    Zwraca dane po jednym elemencie (leniwe ladowanie).
    """
    for element in dane:
        yield element

def czy_jest_obrot(wiersz):
    """
    Sprawdza, czy w danym dniu byl jakikolwiek handel.
    """
    return float(wiersz[5]) > 0

def zrob_slownik(wiersz):
    """
    Zamienia surowa liste na slownik i od razu oblicza zmiane ceny.
    """
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
    """
    Oblicza sume listy wykorzystujac obowiazkowa rekurencje (zamiast sum()).
    """
    if len(lista) == 0:
        return 0
    return lista[0] + suma_rekurencyjna(lista[1:])

def grupuj_pandas(df):
    """
    Grupuje dane po dniach tygodnia (split-apply-combine).
    """
    df = df.copy()
    dni_map = {
        'Monday': 'Poniedziałek', 'Tuesday': 'Wtorek', 'Wednesday': 'Środa',
        'Thursday': 'Czwartek', 'Friday': 'Piątek', 'Saturday': 'Sobota', 'Sunday': 'Niedziela'
    }
    df['dzien'] = df['data'].dt.day_name().map(dni_map)
    kolejnosc = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
    
    wynik = df.groupby('dzien')['wolumen'].mean().reset_index()
    wynik['dzien'] = pd.Categorical(wynik['dzien'], categories=kolejnosc, ordered=True)
    wynik = wynik.sort_values('dzien')
    return wynik

def oblicz_mediane(df, kolumna):
    """Zwraca mediane podanej kolumny"""
    return df[kolumna].median()

def oblicz_odchylenie(df, kolumna):
    """Zwraca odchylenie standardowe podanej kolumny"""
    return df[kolumna].std()