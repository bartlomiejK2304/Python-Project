import streamlit as st
import pandas as pd
from functools import reduce
from dane_funkcje import (
    pobierz_dane, moj_generator, czy_jest_obrot, zrob_slownik, 
    suma_rekurencyjna, grupuj_pandas, oblicz_mediane, oblicz_odchylenie
)
from wykresy import rysuj_matplotlib, rysuj_seaborn, rysuj_plotly, rysuj_altair

def main():
    """
    Glowna czesc programu. Odpowiada za wyswietlanie aplikacji w Streamlit.
    """
    st.title("Projekt z Pythona - Analiza Rynku Gieldowego")
    
    st.header("1. Wstęp i cel projektu")
    st.write("Celem tego projektu jest pobranie danych z darmowego API gieldy kryptowalut (Binance) i przeprowadzenie prostej analizy. Badamy zachowanie ceny Bitcoina (BTC) z ostatnich 100 dni.")
    st.write("Chcemy dowiedziec sie, jakie sa srednie ceny, czy cena zalezy od wolumenu handlu, oraz w jakie dni tygodnia ludzie najczesciej handluja.")

    st.header("2. Pobranie i omowienie danych")
    
    surowe_dane = pobierz_dane()
    generator = moj_generator(surowe_dane)
    przefiltrowane = filter(czy_jest_obrot, generator)
    zmapowane = map(zrob_slownik, przefiltrowane)
    lista_danych = list(zmapowane)
    df = pd.DataFrame(lista_danych)

    st.write("Uzywajac paradygmatu funkcyjnego (map, filter) zamienilismy surowe dane na tabele. Oto poczatek naszej tabeli:")
    st.dataframe(df.head())
    
    st.write("W naszej tabeli mamy nastepujace informacje:")
    st.write("- **data**: Dzien, ktorego dotyczy pomiar")
    st.write("- **otwarcie**: Cena w dolarach na poczatku dnia")
    st.write("- **zamkniecie**: Cena w dolarach na koniec dnia")
    st.write("- **wolumen**: Ilosc sztuk Bitcoina, ktora zostala sprzedana/kupiona tego dnia")

    st.header("3. Podstawowe statystyki (Miary)")
    st.write("Zanim przejdziemy do wykresow, sprawdzmy podstawowe informacje statystyczne o naszych danych, zeby miec punkt odniesienia.")
    
    mediana_ceny = oblicz_mediane(df, 'zamkniecie')
    odchylenie_ceny = oblicz_odchylenie(df, 'zamkniecie')
    
    st.write(f"**Mediana ceny zamkniecia:** {mediana_ceny:.2f} USD (wartosc srodkowa)")
    st.write(f"**Odchylenie standardowe ceny:** {odchylenie_ceny:.2f} USD (mowi nam, jak bardzo ceny skacza wokol sredniej)")
    
    najwiekszy_wolumen = reduce(lambda a, b: a if a['wolumen'] > b['wolumen'] else b, lista_danych)
    st.write(f"**Najwiekszy jednodniowy wolumen (obliczony funkcja reduce):** {najwiekszy_wolumen['wolumen']} sztuk")

    lista_wolumenow = [element['wolumen'] for element in lista_danych]
    suma_wol = suma_rekurencyjna(lista_wolumenow)
    st.write(f"**Calkowity obrot w badanym czasie (obliczony rekurencyjnie):** {suma_wol:.2f} sztuk")

    st.header("4. Analiza i Wykresy")
    
    st.subheader("Jak zmieniala sie cena w czasie? (Matplotlib)")
    st.pyplot(rysuj_matplotlib(df))
    st.write("**Wniosek:** Z powyzszego wykresu mozemy odczytac ogolny trend na rynku. Mozemy zauwazyc, czy cena z biegiem czasu rosnie, maleje, czy utrzymuje sie na jednym poziomie.")

    st.subheader("Czy wartosci sa ze soba powiazane? (Korelacja - Seaborn)")
    st.pyplot(rysuj_seaborn(df))
    st.write("**Wniosek:** Macierz korelacji pokazuje powiazania od -1 do 1. Widzimy, ze otwarcie i zamkniecie maja korelacje bliska 1, co oznacza ze cena nie zmienia sie drastycznie w ciagu jednego dnia. Widzimy tez, ze wolumen slabo wplywa na sama cene.")

    st.subheader("Zaleznosc ceny otwarcia od zamkniecia (Plotly)")
    st.plotly_chart(rysuj_plotly(df))
    st.write("**Wniosek:** Na tym interaktywnym wykresie kropeczki ukladaja sie niemal w idealna linie prosta. To potwierdza nasz wniosek z macierzy korelacji - cena zamkniecia jest bardzo mocno zalezna od tego, z jaka cena rozpoczal sie dzien.")

    st.subheader("W jakie dni handluje sie najwiecej? (Altair)")
    df_grupowane = grupuj_pandas(df)
    st.altair_chart(rysuj_altair(df_grupowane))
    st.write("**Wniosek:** Pogrupowalismy dane po dniach tygodnia uzywajac w Pandas mechanizmu split-apply-combine. Dzieki temu widzimy, czy w weekendy na gieldzie jest spokojniej niz w srodku tygodnia roboczego.")

if __name__ == "__main__":
    main()