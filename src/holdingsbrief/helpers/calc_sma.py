# ~/src/holdingsbrief/helpers/calc_sma.py

import pandas as pd

from holdingsbrief.helpers.fetch_stock_data import get_yf_data
from holdingsbrief.helpers.workbook_info import Workbook, sheet_as_list


def get_settings(workbook: Workbook, verbose: bool = False) -> list[int]:
    settings_url = f"{workbook.url}/export?format=csv&gid={workbook.settings.gid}"
    settings = sheet_as_list(settings_url)

    if not settings:
        raise ValueError("No Settings were Found")

    days = [int(value) for value in settings]

    if verbose:
        print(days)

    return days


def calc_sma(df: pd.DataFrame, days: int = 20) -> float:
    sma = round(df["Close"].rolling(days).mean().iloc[-1], 2)
    return sma


def calc_last_sma(df: pd.DataFrame, days: int = 20) -> float:
    last_sma = round(df["Close"].rolling(days).mean().iloc[-2], 2)
    return last_sma


def calc_slope(df: pd.DataFrame, days: int = 20) -> float:
    slope = round(calc_sma(df, days) - calc_last_sma(df, days), 2)
    return slope


def get_sma(verbose=False) -> pd.DataFrame:
    workbook = Workbook()

    watchlist_url = f"{workbook.url}/export?format=csv&gid={workbook.watchlist.gid}"
    tickers = sheet_as_list(watchlist_url)

    df = get_yf_data(tickers=tickers)
    days = get_settings(workbook, verbose=verbose)

    results = []

    for symbol in tickers:
        df_itr = df[df["Ticker"] == symbol]

        closing_price = df_itr["Close"].iloc[-1]

        for day in days:
            sma = calc_sma(df=df_itr, days=day)
            last_sma = calc_last_sma(df=df_itr, days=day)
            slope = calc_slope(df=df_itr, days=day)

            results.append(
                {
                    "Ticker": symbol,
                    "SMA Days": day,
                    "Close": closing_price,
                    "SMA": sma,
                    "Last SMA": last_sma,
                    "Slope": slope,
                }
            )

            if verbose:
                print(
                    f"{symbol} | {day} SMA | "
                    f"Close: ${closing_price} | "
                    f"SMA: ${sma} | "
                    f"Last SMA: ${last_sma} | "
                    f"Slope: {slope}"
                )

    return pd.DataFrame(results)


if __name__ == "__main__":
    get_sma(verbose=True)
