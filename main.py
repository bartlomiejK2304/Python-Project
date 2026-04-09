import streamlit as st
import pandas as pd
from functools import reduce
from dane_funkcje import pobierz_dane, moj_generator, czy_jest_obrot, zrob_slownik, suma_rekurencyjna, grupuj_pandas
from wykresy import rysuj_matplotlib, rysuj_seaborn, rysuj_plotly, rysuj_altair

def main():
    """
    Glowna czesc programu
    """
    st.title("Projekt z Pythona - Analiza Gieldy")

    surowe_dane = pobierz_dane()
    
    generator = moj_generator(surowe_dane)
    
    przefiltrowane = filter(czy_jest_obrot, generator)
    
    zmapowane = map(zrob_slownik, przefiltrowane)
    
    lista_danych = list(zmapowane)
    
    najwiekszy_wolumen = reduce(lambda a, b: a if a['wolumen'] > b['wolumen'] else b, lista_danych)
    
    st.write("Najwiekszy wolumen z uzyciem funkcji reduce wynosi:", najwiekszy_wolumen['wolumen'])
    
    lista_wolumenow = [element['wolumen'] for element in lista_danych]
    suma_wol = suma_rekurencyjna(lista_wolumenow)
    st.write("Calkowity obrot obliczony rekurencja:", suma_wol)

    df = pd.DataFrame(lista_danych)
    st.write("Tabela z danymi:")
    st.dataframe(df)

    st.write("Wykres Matplotlib:")
    st.pyplot(rysuj_matplotlib(df))

    st.write("Analiza - Korelacja Seaborn:")
    st.pyplot(rysuj_seaborn(df))

    st.write("Wykres Plotly:")
    st.plotly_chart(rysuj_plotly(df))

    st.write("Analiza w Altair:")
    df_grupowane = grupuj_pandas(df)
    st.altair_chart(rysuj_altair(df_grupowane))

if __name__ == "__main__":
    main()