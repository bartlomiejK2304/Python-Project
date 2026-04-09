import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
import numpy as np

def rysuj_matplotlib(df):
    fig, ax = plt.subplots()
    ax.plot(df['data'], df['zamkniecie'])
    ax.set_title("Cena BTC w czasie")
    ax.set_xlabel("Data")
    ax.set_ylabel("Cena (USD)")
    plt.xticks(rotation=45)
    return fig


def rysuj_seaborn(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    korelacja = df[['otwarcie', 'zamkniecie', 'wolumen']].corr()

    sns.heatmap(
        korelacja,
        annot=True,
        cmap='RdBu_r',
        center=0,
        linewidths=1,
        linecolor='black',
        fmt=".2f",
        ax=ax
    )

    return fig


def rysuj_plotly(df):
    x = list(df['otwarcie'])
    y = list(df['zamkniecie'])

    n = len(x)
    sx = sum(x) / n
    sy = sum(y) / n

    a = sum((x[i] - sx)*(y[i] - sy) for i in range(n)) / sum((x[i] - sx)**2 for i in range(n))
    b = sy - a*sx

    fig = px.scatter(df, x='otwarcie', y='zamkniecie')

    x_lin = np.linspace(min(x), max(x), 100)
    y_lin = a * x_lin + b

    fig.add_scatter(x=x_lin, y=y_lin, mode='lines', name='Trend', line=dict(color='red'))

    return fig


def rysuj_altair(df):
    return alt.Chart(df).mark_bar().encode(
        x=alt.X('dzien', sort=None),
        y='wolumen'
    )