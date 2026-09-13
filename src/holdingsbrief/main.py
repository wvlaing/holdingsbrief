# ~/src/holdingsbrief/main.py

import os

from dotenv import load_dotenv

from holdingsbrief.helpers.calc_sma import get_sma
from holdingsbrief.helpers.gmail_api import send_email

load_dotenv()

url = os.environ["WORKBOOK_URL"]
emails = os.environ["SUBSCRIBERS"]


def create_sma_report() -> str:
    sma_df = get_sma()

    sections = []

    for days in sma_df["SMA Days"].unique():
        section = sma_df[sma_df["SMA Days"] == days]
        section = section.sort_values("Slope")

        table = section[["Ticker", "Slope"]].to_html(
            index=False,
            float_format=lambda x: f"{x:.2f}",
        )

        sections.append(
            f"""
            <h2>{days} Day SMA Slope</h2>
            {table}
            """
        )

    return "".join(sections)


html = f"""
<h1>Portfolio SMA Slope Report</h1>

{create_sma_report()}

<p>
    <a href="{url}">
        Link to Google Sheet to make adjustments
    </a>
</p>
"""


send_email(
    to=emails,
    subject="SMA Stock Report V1",
    body=html,
)
