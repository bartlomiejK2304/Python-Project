import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt

def rysuj_matplotlib(df):
    """
    Zwykly wykres liniowy
    """
    fig, ax = plt.subplots()
    ax.plot(df['data'], df['zamkniecie'])
    plt.xticks(rotation=45)
    return fig

def rysuj_seaborn(df):
    """
    Wykres korelacji do analizy
    """
    fig, ax = plt.subplots()
    korelacja = df[['otwarcie', 'zamkniecie', 'wolumen']].corr()
    sns.heatmap(korelacja, annot=True, ax=ax)
    return fig

def rysuj_plotly(df):
    """
    Wykres punktowy zaleznosci miedzy otwarciem a zamknieciem
    """
    fig = px.scatter(df, x='otwarcie', y='zamkniecie', title="Zaleznosc cen")
    return fig

def rysuj_altair(df_grupowane):
    """
    Wykres slupkowy z dniami tygodnia
    """
    wykres = alt.Chart(df_grupowane).mark_bar().encode(
        x='dzien',
        y='wolumen'
    ).properties(
        title="Sredni wolumen w dniach"
    )
    return wykres