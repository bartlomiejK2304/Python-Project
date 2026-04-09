import streamlit as st
import pandas as pd
from functools import reduce

from dane_funkcje import (
    pobierz_dane, moj_generator, czy_jest_obrot, zrob_slownik,
    suma_rekurencyjna, grupuj_pandas, oblicz_mediane, oblicz_odchylenie
)

from wykresy import (
    rysuj_matplotlib, rysuj_seaborn, rysuj_plotly, rysuj_altair
)

def main():
    """
    Główna funkcja aplikacji integrująca interfejs Streamlit.
    """
    st.set_page_config(layout="wide") # Szerszy widok dla lepszej czytelnosci
    st.title("Analiza rynku BTC – eksploracja danych i zależności")

    st.header("1. Dane")
    st.write("Na podstawie danych z API giełdy Binance badamy zachowanie Bitcoina z ostatnich 100 dni.")

    surowe_dane = pobierz_dane()
    generator = moj_generator(surowe_dane)
    przefiltrowane = filter(czy_jest_obrot, generator)
    zmapowane = map(zrob_slownik, przefiltrowane)
    lista_danych = list(zmapowane)

    df = pd.DataFrame(lista_danych)
    df.index = df.index + 1

    st.dataframe(df)

    st.header("2. Statystyki i wyliczenia funkcyjne")
    
    # Ladne kolumny w Streamlit do pokazania statystyk
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Średnia cena", f"{df['zamkniecie'].mean():.2f} USD")
    with col2:
        st.metric("Mediana", f"{df['zamkniecie'].median():.2f} USD")
    with col3:
        st.metric("Min. cena", f"{df['zamkniecie'].min():.2f} USD")
    with col4:
        st.metric("Max. cena", f"{df['zamkniecie'].max():.2f} USD")

    st.write("---")
    
    # Nowa funkcja analizujaca dni na plusie i minusie (uzycie filter i lambda)
    dni_wzrostowe = list(filter(lambda x: x['zmiana_ceny'] > 0, lista_danych))
    dni_spadkowe = list(filter(lambda x: x['zmiana_ceny'] <= 0, lista_danych))
    
    st.write(f"**Analiza zachowania ceny:** Przez badane 100 dni rynek rósł w **{len(dni_wzrostowe)}** dni, a spadał w **{len(dni_spadkowe)}** dni.")

    # Wykorzystanie reduce
    najwiekszy = reduce(
        lambda a, b: a if a['wolumen'] > b['wolumen'] else b,
        lista_danych
    )
    st.write(f"**Największy jednodniowy wolumen (Reduce):** {najwiekszy['wolumen']:.2f} sztuk")

    # Wykorzystanie rekurencji
    suma = suma_rekurencyjna([x['wolumen'] for x in lista_danych])
    st.write(f"**Całkowity wolumen w badanym okresie (Rekurencja):** {suma:.2f} sztuk")

    st.header("3. Wykresy i Wnioski")

    # Dzielimy ekran na dwie czesci, zeby wykresy ladniej wygladaly
    wykres_col1, wykres_col2 = st.columns(2)

    with wykres_col1:
        st.subheader("Cena w czasie (Matplotlib)")
        st.pyplot(rysuj_matplotlib(df))
        st.info("Widoczny jest ogólny trend rynkowy w badanym okresie. Wykres pozwala nam określić, czy rynek znajduje się w fazie wzrostów czy spadków.")

        st.subheader("Otwarcie vs Zamknięcie (Plotly)")
        st.plotly_chart(rysuj_plotly(df), use_container_width=True)
        st.info("Punkty tworzą niemal linię prostą – silna zależność liniowa. Kolor zielony oznacza dzień zakończony na plusie.")

    with wykres_col2:
        st.subheader("Korelacja (Seaborn)")
        st.pyplot(rysuj_seaborn(df))
        st.info("Bardzo silna zależność między ceną otwarcia i zamknięcia (~0.98). Wolumen ma znacznie słabszy (ujemny) wpływ na cenę.")

        st.subheader("Wolumen wg dni tygodnia (Altair)")
        df_grup = grupuj_pandas(df)
        st.altair_chart(rysuj_altair(df_grup), use_container_width=True)
        st.info("Największa aktywność przypada zazwyczaj na dni robocze. Wynika to z faktu, że w weekendy inwestorzy rzadziej zawierają transakcje.")

if __name__ == "__main__":
    main()