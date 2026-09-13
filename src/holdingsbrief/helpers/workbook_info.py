# ~/src/holdingsbrief/helpers/read_workbook_info.py

import csv
import io
import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class Worksheet:
    def __init__(self, workbook: Workbook, name: str, gid: str):
        self.workbook = workbook
        self.name = name
        self.gid = gid


class Workbook:
    def __init__(self):
        url = os.getenv("WORKBOOK_URL")
        watchlist_gid = os.getenv("WATCHLIST_GID")
        settings_gid = os.getenv("SETTINGS_GID")

        if url is None:
            raise ValueError("WORKBOOK_URL is not set")
        if watchlist_gid is None:
            raise ValueError("WATCHLIST_GID is not set")
        if settings_gid is None:
            raise ValueError("SETTINGS_GID is not set")

        self.url = url

        self.settings = Worksheet(
            self,
            "settings",
            settings_gid,
        )

        self.watchlist = Worksheet(
            self,
            "watchlist",
            watchlist_gid,
        )


def request_sheet(url):
    r = httpx.get(url, follow_redirects=True)
    r.raise_for_status()

    response = io.StringIO(r.text)

    return response


def convert_csv_to_list(response: io.StringIO) -> list[str]:
    reader = csv.reader(response)
    next(reader)  # skip header row

    return [row[0].strip() for row in reader if row and row[0].strip()]


def sheet_as_list(url, verbose: bool = False) -> list[str]:

    response = request_sheet(url)

    contents = convert_csv_to_list(response)

    if verbose:
        print(contents)

    return contents


if __name__ == "__main__":
    workbook = Workbook()

    watchlist_url = f"{workbook.url}/export?format=csv&gid={workbook.watchlist.gid}"
    settings_url = f"{workbook.url}/export?format=csv&gid={workbook.settings.gid}"

    watchlist = sheet_as_list(watchlist_url)
    settings = sheet_as_list(settings_url)

    print(" ")
    print(f"{settings}")
    print(" ")
    print(f"{watchlist}")
    print(" ")
