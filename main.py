import streamlit as st
import pandas as pd
from functools import reduce

from dane_funkcje import (
    pobierz_dane, moj_generator, czy_jest_obrot, zrob_slownik,
    suma_rekurencyjna, grupuj_pandas, regresja_sklearn
)

from wykresy import (
    rysuj_matplotlib, rysuj_seaborn, rysuj_plotly, rysuj_altair
)


def main():
    st.set_page_config(layout="wide")

    st.title("Projekt zaliczeniowy: Analiza rynku kryptowalut na przykładzie kursu Bitcoin (BTC/USDT)")

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
    st.info("""
Widoczny jest silny spadek ceny, a następnie stabilizacja.
Rynek przechodzi w fazę konsolidacji.
""")

    st.subheader("Macierz korelacji")
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.pyplot(rysuj_seaborn(df))
    st.info("""
Bardzo silna korelacja (~0.98) między ceną otwarcia i zamknięcia.
Wolumen ma słabszy wpływ na cenę.
""")

    st.subheader("Otwarcie vs Zamknięcie + regresja")
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.plotly_chart(rysuj_plotly(df))
    st.info("""
Zależność liniowa między cenami. Linia regresji potwierdza silną zależność.
""")

    st.subheader("Wolumen wg dni tygodnia")
    df_g = grupuj_pandas(df)
    col1, col2, col3 = st.columns([1,5,1])
    with col2:
        st.altair_chart(rysuj_altair(df_g))
    st.info("""
Największa aktywność w dni robocze, niższa w weekendy.
""")


if __name__ == "__main__":
    main()