import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
import numpy as np
from sklearn.linear_model import LinearRegression

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
    X = df[['otwarcie']].values
    y = df['zamkniecie'].values

    model = LinearRegression()
    model.fit(X, y)

    fig = px.scatter(
        df,
        x='otwarcie',
        y='zamkniecie',
        title="Otwarcie vs Zamknięcie + regresja"
    )

    x_lin = np.linspace(min(X), max(X), 100).reshape(-1, 1)
    y_lin = model.predict(x_lin)

    fig.add_scatter(
        x=x_lin.flatten(),
        y=y_lin,
        mode='lines',
        name='Regresja',
        line=dict(color='red')
    )

    return fig


def rysuj_altair(df):
    return alt.Chart(df).mark_bar().encode(
        x=alt.X('dzien', sort=None, title="Dzień tygodnia"),
        y=alt.Y('wolumen', title="Średni wolumen"),
        tooltip=['dzien', 'wolumen']
    )