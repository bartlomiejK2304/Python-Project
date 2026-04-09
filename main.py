import streamlit as st
import pandas as pd
from functools import reduce

from dane_funkcje import (
    pobierz_dane, moj_generator, czy_jest_obrot, zrob_slownik,
    suma_rekurencyjna, grupuj_pandas
)

from wykresy import (
    rysuj_matplotlib, rysuj_seaborn, rysuj_plotly, rysuj_altair
)


def main():
    st.set_page_config(layout="wide")

    st.title("Projekt zaliczeniowy: Analiza rynku kryptowalut na przykładzie kursu Bitcoin (BTC/USDT) z ostatnich 100 dni")

    st.header("1. Wstęp i dane")
    st.write("Projekt analizuje zachowanie ceny Bitcoina na podstawie danych z API Binance.")

    dane = list(map(zrob_slownik, filter(czy_jest_obrot, moj_generator(pobierz_dane()))))
    df = pd.DataFrame(dane)
    df.index += 1

    st.dataframe(df)

    st.header("2. Statystyki opisowe")

    dni_wzrostowe = len(list(filter(lambda x: x['zmiana_ceny'] > 0, dane)))
    dni_spadkowe = len(dane) - dni_wzrostowe
    suma = suma_rekurencyjna([x['wolumen'] for x in dane])

    st.write(f"""
Średnia cena zamknięcia: {df['zamkniecie'].mean():.2f} USD  
Mediana ceny: {df['zamkniecie'].median():.2f} USD  

Dni wzrostowe: {dni_wzrostowe}  
Dni spadkowe: {dni_spadkowe}  

Całkowity wolumen: {suma:.2f} BTC
""")

    st.header("3. Wykresy i analiza")

    st.subheader("Cena BTC w czasie")
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.pyplot(rysuj_matplotlib(df))
    st.info("Wyraźny spadek ceny na początku, następnie stabilizacja rynku.")

    st.subheader("Macierz korelacji")
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.pyplot(rysuj_seaborn(df))
    st.info("Silna zależność między ceną otwarcia i zamknięcia (~0.98).")

    st.subheader("Otwarcie vs Zamknięcie")
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.plotly_chart(rysuj_plotly(df))
    st.info("Punkty układają się liniowo – wysoka zależność.")

    st.subheader("Wolumen wg dni tygodnia")
    df_g = grupuj_pandas(df)
    col1, col2, col3 = st.columns([1,5,1])
    with col2:
        st.altair_chart(rysuj_altair(df_g))
    st.info("Większy wolumen w dni robocze, mniejszy w weekendy.")

    st.header("4. Wnioski końcowe")
    st.write("""
Rynek Bitcoina w analizowanym okresie przeszedł spadek, a następnie stabilizację.
Ceny są silnie zależne od siebie w krótkim okresie, a aktywność handlowa
jest większa w dni robocze niż w weekendy.
""")


if __name__ == "__main__":
    main()