import streamlit as st
import pandas as pd
from functools import reduce

from dane_funkcje import (
    pobierz_dane, moj_generator, czy_jest_obrot, zrob_slownik,
    suma_rekurencyjna, grupuj_pandas, oblicz_mediane, oblicz_odchylenie,
    regresja_liniowa
)

from wykresy import (
    rysuj_matplotlib, rysuj_seaborn, rysuj_plotly, rysuj_altair
)


def main():
    st.set_page_config(layout="wide")

    st.title("Analiza rynku BTC – projekt")

    surowe_dane = pobierz_dane()
    dane = list(map(zrob_slownik, filter(czy_jest_obrot, moj_generator(surowe_dane))))

    df = pd.DataFrame(dane)
    df.index += 1

    st.dataframe(df)

    st.header("Statystyki")

    st.write(f"Średnia: {df['zamkniecie'].mean():.2f}")
    st.write(f"Mediana: {df['zamkniecie'].median():.2f}")

    dni_wzrostowe = len(list(filter(lambda x: x['zmiana_ceny'] > 0, dane)))
    dni_spadkowe = len(dane) - dni_wzrostowe

    st.write(f"Wzrostowe: {dni_wzrostowe}, spadkowe: {dni_spadkowe}")

    suma = suma_rekurencyjna([x['wolumen'] for x in dane])
    st.write(f"Suma wolumenu: {suma:.2f}")

    # 🔥 REGRESJA
    st.header("Regresja liniowa")

    a, b = regresja_liniowa(df)
    st.write(f"y = {a:.4f}x + {b:.2f}")

    # 📊 WYKRESY

    st.subheader("Cena")
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.pyplot(rysuj_matplotlib(df))

    st.subheader("Korelacja")
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.pyplot(rysuj_seaborn(df))

    st.subheader("Scatter + regresja")
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        st.plotly_chart(rysuj_plotly(df))

    st.subheader("Wolumen dni")
    df_g = grupuj_pandas(df)
    col1, col2, col3 = st.columns([1,5,1])
    with col2:
        st.altair_chart(rysuj_altair(df_g))


if __name__ == "__main__":
    main()