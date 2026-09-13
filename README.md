# HoldingsBrief

A small automation that keeps an eye on a stock watchlist and flags what might be worth a closer look.

HoldingsBrief pulls the watchlist from a Google Sheet, calculates simple moving average (SMA) trends for each ticker, and emails a daily report. The report provides a list of SMA slope changes (i.e. momentum shifting up or down) so they know what's worth digging into further.

## What it does

- Reads a ticker watchlist and SMA settings from a Google Sheet
- Pulls historical price data via [yfinance](https://pypi.org/project/yfinance/)
- Calculates SMA slope for each ticker across configurable day ranges
- Emails a list of tickers along with the slope of their SMA change between the two most recent market closes

## Setup

1. Clone the repo and install dependencies:

2. Copy `.env.example` to `.env` and fill in:
   - `WORKBOOK_URL` — link to your Google Sheet
   - `WATCHLIST_GID` / `SETTINGS_GID` — sheet tab IDs for your watchlist and SMA settings
   - `SUBSCRIBERS` — comma-separated email(s) to send the report to
3. To setup Gmail's API go here -> [Google's Python quickstart](https://developers.google.com/gmail/api/quickstart/python)
    By default, you'll need to place the credentials.json and token.json in the projects root

## Usage

This fetches the latest data, computes SMA slopes, and sends the report. I have it executed on a debian server daily around 4:30 est

## Notes

This was built for personal use, so it's intentionally simple meaning no dashboard, no database, just a daily nudge toward what deserves a closer look.

## License

MIT