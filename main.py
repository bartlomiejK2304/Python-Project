import streamlit as st
import pandas as pd
from functools import reduce

from dane_funkcje import (
    pobierz_dane, moj_generator, czy_jest_obrot, zrob_slownik,
    suma_wolumenow, grupuj_pandas, oblicz_mediane, oblicz_odchylenie
)

from wykresy import (
    rysuj_matplotlib, rysuj_seaborn, rysuj_plotly, rysuj_altair
)


def main():
    st.title("Projekt z Pythona - Analiza Rynku Giełdowego")

    st.header("1. Wstęp")
    st.write("Analiza ceny Bitcoina (BTC) z ostatnich 100 dni.")

    st.header("2. Dane")

    surowe_dane = pobierz_dane()
    generator = moj_generator(surowe_dane)
    przefiltrowane = filter(czy_jest_obrot, generator)
    zmapowane = map(zrob_slownik, przefiltrowane)
    lista_danych = list(zmapowane)

    df = pd.DataFrame(lista_danych)
    df.index = df.index + 1  

    st.dataframe(df)

    st.header("3. Statystyki")

    st.write(f"Mediana: {df['zamkniecie'].median():.2f} USD")
    st.write(f"Odchylenie: {df['zamkniecie'].std():.2f} USD")
    st.write(f"Średnia: {df['zamkniecie'].mean():.2f} USD")
    st.write(f"Min: {df['zamkniecie'].min():.2f} USD")
    st.write(f"Max: {df['zamkniecie'].max():.2f} USD")

    zmiennosc = df['zamkniecie'].max() - df['zamkniecie'].min()
    st.write(f"Zmienność: {zmiennosc:.2f} USD")

    najwiekszy = reduce(
        lambda a, b: a if a['wolumen'] > b['wolumen'] else b,
        lista_danych
    )
    st.write(f"Największy wolumen: {najwiekszy['wolumen']:.2f}")

    suma = suma_wolumenow([x['wolumen'] for x in lista_danych])
    st.write(f"Całkowity wolumen: {suma:.2f}")

    st.write("Macierz korelacji:")
    st.dataframe(df[['otwarcie', 'zamkniecie', 'wolumen']].corr())

    st.header("4. Wykresy")

    st.subheader("Cena w czasie")
    st.pyplot(rysuj_matplotlib(df))
    st.write("Trend spadkowy, potem stabilizacja rynku.")

    st.subheader("Korelacja")
    st.pyplot(rysuj_seaborn(df))
    st.write("Otwarcie i zamknięcie są silnie powiązane.")

    st.subheader("Otwarcie vs Zamknięcie")
    st.plotly_chart(rysuj_plotly(df))
    st.write("Silna zależność liniowa między cenami.")

    st.subheader("Wolumen wg dni tygodnia")
    df_grup = grupuj_pandas(df)
    st.altair_chart(rysuj_altair(df_grup))
    st.write("Największa aktywność w środku tygodnia.")


if __name__ == "__main__":
    main()