import pandas as pd
import plotly.express as px
import datetime
import pytz
import os

DIR = os.getcwd()#.replace("/build/exe.linux-x86_64-3.9/", "")
DATE = datetime.datetime.now(
    pytz.timezone('UTC')
    ).strftime("%Y-%m-%d %H:%M:%S")


def make_plot(data: pd.DataFrame) -> px.bar:
    fig = px.bar(
        data, 
        title = f"BTCEUR Arbitrage Opportunity at {DATE}",
        x = "exchange", 
        y = "price", 
        color = "price",
        color_continuous_scale = px.colors.diverging.BrBG,
        text = "price",
        log_y = True,
    )
    fig.update_layout(
        font_size = 16,
        paper_bgcolor = "white",
        plot_bgcolor = "white",
        margin = dict(b = 0, r = 0, t = 45, l = 0)
    )
    return fig


def save_plot(fig: px.bar) -> None:
    fig.write_image(f"{DIR}/plots/BTCEUR.png", width=800, height=200)#, width = 800, height = 200)


def main(data: pd.DataFrame) -> None:
    fig = make_plot(data)
    save_plot(fig)


if __name__ == "__main__":
    data = pd.DataFrame({
        "exchange": ["FTX", "BINANCE", "BITPANDA"],
        "pair": ["BTCEUR", "BTCEUR", "BTCEUR"],
        "price": [20351.00, 20360.89, 20378.18]
    })
    main(data)