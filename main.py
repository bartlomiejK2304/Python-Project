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
    
    # SPRECYZOWANY TYTUŁ
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
    st.write(f"**Największy jednodniowy wolumen (obliczony funkcją reduce):** {najwiekszy['wolumen']:.2f} sztuk BTC")

    suma = suma_rekurencyjna([x['wolumen'] for x in lista_danych])
    st.write(f"**Całkowity wolumen w badanym okresie (obliczony rekurencją):** {suma:.2f} sztuk BTC")

    st.header("3. Analiza graficzna i Wnioski")
    st.write("W poniższej sekcji prezentujemy cztery różne wykresy. Każdy z nich został wygenerowany za pomocą innej biblioteki i służy do zbadania innych właściwości naszego zbioru danych.")

    # Wykres 1
    st.subheader("3.1. Zmiana ceny w czasie (Matplotlib)")
    st.pyplot(rysuj_matplotlib(df))
    st.info("Wykres liniowy przedstawia, jak kształtowała się cena zamknięcia Bitcoina na przestrzeni badanych 100 dni. Pozwala to łatwo zaobserwować główne trendy rynkowe – okresy dynamicznych wzrostów oraz korekt i spadków. Dzięki temu zyskujemy ogólny pogląd na kondycję rynku i widzimy, w jakich datach przypadały lokalne maksima i minima cenowe.")

    # Wykres 2
    st.subheader("3.2. Macierz korelacji zmiennych (Seaborn)")
    st.pyplot(rysuj_seaborn(df))
    st.info("Macierz korelacji pozwala nam zbadać siłę powiązań między różnymi wskaźnikami liczbowymi. Wartość bliska 1.0 (ciemnoczerwona) oznacza bardzo silną zależność dodatnią – widzimy tu, że cena otwarcia i zamknięcia danego dnia idą niemal idealnie w parze. Z kolei korelacja wolumenu z ceną jest lekko ujemna (kolor jasnoniebieski), co sugeruje, że przy wyższych cenach aktywność handlowa w tym okresie była nieco mniejsza (lub przy spadkach inwestorzy chętniej sprzedawali).")

    # Wykres 3
    st.subheader("3.3. Zależność: Otwarcie vs Zamknięcie (Plotly)")
    st.plotly_chart(rysuj_plotly(df), use_container_width=True)
    st.info("Ten interaktywny wykres punktowy szczegółowo obrazuje relację między ceną otwarcia a zamknięcia dla każdego pojedynczego dnia. Punkty ułożyły się wzdłuż przekątnej, co wizualnie potwierdza naszą silną korelację z poprzedniego wykresu. Dodatkowo zastosowaliśmy formatowanie warunkowe: zielone kropki to dni wzrostowe (cena zamknięcia wyższa niż otwarcia), a czerwone to dni spadkowe. Dzięki temu łatwo zidentyfikować dni o nietypowo dużej zmienności, czyli te punkty, które najmocniej odstają od głównej, ukośnej linii.")

    # Wykres 4
    st.subheader("3.4. Aktywność rynku w dniach tygodnia (Altair)")
    df_grup = grupuj_pandas(df)
    st.altair_chart(rysuj_altair(df_grup), use_container_width=True)
    st.info("Wykres słupkowy ukazuje średni wolumen obrotu z podziałem na konkretne dni tygodnia. Aby go uzyskać, wykorzystaliśmy wbudowany w bibliotekę Pandas paradygmat split-apply-combine (pogrupowanie danych po dniu, wyliczenie średniej i ponowne złączenie). Bardzo często można tu zauważyć prawidłowość polegającą na tym, że w weekendy (sobota, niedziela) obrót nieco spada, co wynika z mniejszego zaangażowania inwestorów instytucjonalnych w dni wolne od pracy.")

if __name__ == "__main__":
    main()