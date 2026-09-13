# ~/src/holdingsbrief/helpers/read_watchlist.py

import pandas as pd
import yfinance as yf


def get_yf_data(tickers: list[str], verbose: bool = False) -> pd.DataFrame:
    data = yf.download(
        tickers,
        period="365d",
        auto_adjust=False,
        progress=False,
    )

    if data is None or data.empty:
        raise ValueError("yfinance returned no data")

    df = (
        data[["Close", "Volume"]]
        .stack(level="Ticker", future_stack=True)
        .reset_index()
        .sort_values(["Ticker", "Date"])
        .reset_index(drop=True)
        .round({"Close": 2})
    )

    if verbose:
        print(df)

    return df


if __name__ == "__main__":
    from holdingsbrief.helpers.workbook_info import Workbook, sheet_as_list

    workbook = Workbook()
    watchlist_url = f"{workbook.url}/export?format=csv&gid={workbook.watchlist.gid}"
    tickers = sheet_as_list(watchlist_url)

    print(" ")

    get_yf_data(tickers, verbose=True)

    print(" ")
