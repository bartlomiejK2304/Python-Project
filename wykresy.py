import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt

def rysuj_matplotlib(df):
    """
    Wykres liniowy ceny zamknięcia
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
    Macierz korelacji
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    korelacja = df[['otwarcie', 'zamkniecie', 'wolumen']].corr()
    sns.heatmap(korelacja, annot=True, cmap='coolwarm', ax=ax)
    return fig


def rysuj_plotly(df):
    """
    Scatter: otwarcie vs zamknięcie
    """
    fig = px.scatter(
        df,
        x='otwarcie',
        y='zamkniecie',
        title="Zależność: Otwarcie vs Zamknięcie"
    )
    return fig


def rysuj_altair(df_grupowane):
    """
    Wykres słupkowy – dni tygodnia
    """
    wykres = alt.Chart(df_grupowane).mark_bar().encode(
        x=alt.X('dzien', sort=None, title="Dzień tygodnia"),
        y=alt.Y('wolumen', title="Średni wolumen")
    ).properties(
        title="Średni wolumen w dniach tygodnia"
    )
    return wykres