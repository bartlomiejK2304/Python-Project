import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt

def rysuj_matplotlib(df):
    """
    Rysuje wykres liniowy dla ceny zamkniecia.
    """
    fig, ax = plt.subplots()
    ax.plot(df['data'], df['zamkniecie'])
    ax.set_title("Cena zamknięcia BTC w czasie")
    ax.set_xlabel("Data")
    ax.set_ylabel("Cena (USD)")
    plt.xticks(rotation=45)
    return fig

def rysuj_seaborn(df):
    """
    Tworzy macierz korelacji, aby zbadac zaleznosci miedzy kolumnami.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    korelacja = df[['otwarcie', 'zamkniecie', 'wolumen']].corr()
    sns.heatmap(
        korelacja, annot=True, cmap='RdBu_r', center=0,
        linewidths=1, linecolor='black', fmt=".2f", ax=ax
    )
    ax.set_title("Macierz korelacji")
    return fig

def rysuj_plotly(df):
    """
    Generuje interaktywny wykres punktowy zaleznotsci otwarcia od zamkniecia.
    Koloruje punkty na podstawie tego, czy dzien byl na plus czy na minus.
    """
    fig = px.scatter(
        df, x='otwarcie', y='zamkniecie', 
        color=df['zmiana_ceny'] > 0,
        color_discrete_map={True: 'green', False: 'red'},
        title="Zależność: Otwarcie vs Zamknięcie (Zielone = Dzień na plus)"
    )
    return fig

def rysuj_altair(df_grupowane):
    """
    Rysuje slupki ze srednim wolumenem dla dni tygodnia.
    """
    wykres = alt.Chart(df_grupowane).mark_bar().encode(
        x=alt.X('dzien', sort=None, title="Dzień tygodnia"),
        y=alt.Y('wolumen', title="Średni wolumen"),
        tooltip=['dzien', 'wolumen']
    ).properties(
        title="Średni wolumen w dniach tygodnia"
    )
    return wykres