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
    st.set_page_config(layout="wide")

    st.title("Projekt zaliczeniowy: Analiza rynku kryptowalut na przykładzie kursu Bitcoin (BTC/USDT) z ostatnich 100 dni")

    st.header("1. Wstęp i omówienie danych")
    st.write("Celem projektu jest praktyczne wykorzystanie paradygmatu funkcyjnego w Pythonie do pobrania, przetworzenia i wizualizacji rzeczywistych danych. Analizujemy zachowanie najpopularniejszej kryptowaluty – Bitcoina – pobierając dane z publicznego API giełdy Binance.")

    surowe_dane = pobierz_dane()
    generator = moj_generator(surowe_dane)
    przefiltrowane = filter(czy_jest_obrot, generator)
    zmapowane = map(zrob_slownik, przefiltrowane)
    lista_danych = list(zmapowane)

    df = pd.DataFrame(lista_danych)
    df.index = df.index + 1

    st.dataframe(df)

    st.header("2. Statystyki i wyliczenia funkcyjne")

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

    dni_wzrostowe = list(filter(lambda x: x['zmiana_ceny'] > 0, lista_danych))
    dni_spadkowe = list(filter(lambda x: x['zmiana_ceny'] <= 0, lista_danych))

    st.write(f"**Analiza zachowania ceny:** Przez badane 100 dni rynek rósł w **{len(dni_wzrostowe)}** dni, a spadał w **{len(dni_spadkowe)}** dni.")

    najwiekszy = reduce(
        lambda a, b: a if a['wolumen'] > b['wolumen'] else b,
        lista_danych
    )
    st.write(f"**Największy jednodniowy wolumen (reduce):** {najwiekszy['wolumen']:.2f} BTC")

    suma = suma_rekurencyjna([x['wolumen'] for x in lista_danych])
    st.write(f"**Całkowity wolumen (rekurencja):** {suma:.2f} BTC")

    st.header("3. Analiza graficzna i wnioski")

   
    st.subheader("3.1. Zmiana ceny w czasie (Matplotlib)")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(rysuj_matplotlib(df))
    st.info("Widoczny trend spadkowy, a następnie stabilizacja rynku (konsolidacja).")

    
    st.subheader("3.2. Macierz korelacji (Seaborn)")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(rysuj_seaborn(df))
    st.info("Bardzo silna korelacja między ceną otwarcia i zamknięcia (~0.98). Wolumen ma słabszy wpływ.")

    st.subheader("3.3. Otwarcie vs Zamknięcie (Plotly)")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(rysuj_plotly(df), use_container_width=False)
    st.info("Silna zależność liniowa – punkty układają się wzdłuż prostej.")

  
    st.subheader("3.4. Wolumen wg dni tygodnia (Altair)")
    df_grup = grupuj_pandas(df)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.altair_chart(rysuj_altair(df_grup), use_container_width=False)
    st.info("Największa aktywność w dni robocze, niższa w weekendy.")


if __name__ == "__main__":
    main()