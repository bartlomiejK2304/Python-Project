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

    st.header("1. Wstęp i cel projektu")
    st.write("Analiza ceny Bitcoina (BTC) z ostatnich 100 dni na podstawie danych z API Binance.")

    st.header("2. Pobranie danych")

    surowe_dane = pobierz_dane()
    generator = moj_generator(surowe_dane)
    przefiltrowane = filter(czy_jest_obrot, generator)
    zmapowane = map(zrob_slownik, przefiltrowane)
    lista_danych = list(zmapowane)

    df = pd.DataFrame(lista_danych)

    st.write(f"Tabela zawiera {len(df)} dni:")
    st.dataframe(df)

    st.header("3. Statystyki")

    mediana = oblicz_mediane(df, 'zamkniecie')
    odchylenie = oblicz_odchylenie(df, 'zamkniecie')

    st.write(f"Mediana: {mediana:.2f} USD")
    st.write(f"Odchylenie standardowe: {odchylenie:.2f} USD")

    najwiekszy = reduce(
        lambda a, b: a if a['wolumen'] > b['wolumen'] else b,
        lista_danych
    )
    st.write(f"Największy wolumen: {najwiekszy['wolumen']:.2f}")

    lista_wolumenow = [x['wolumen'] for x in lista_danych]
    suma = suma_wolumenow(lista_wolumenow)

    st.write(f"Całkowity wolumen: {suma:.2f}")

    st.header("4. Wykresy")

    st.subheader("Cena w czasie")
    st.pyplot(rysuj_matplotlib(df))

    st.subheader("Korelacja")
    st.pyplot(rysuj_seaborn(df))

    st.subheader("Otwarcie vs Zamknięcie")
    st.plotly_chart(rysuj_plotly(df))

    st.subheader("Wolumen wg dni tygodnia")
    df_grup = grupuj_pandas(df)
    st.altair_chart(rysuj_altair(df_grup))


if __name__ == "__main__":
    main()