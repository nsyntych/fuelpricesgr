"""Module used to fetch data
"""
import enum
import logging
import pathlib
import re
import shutil
import sys

import bs4
import requests

# The base URL
BASE_URL = 'http://www.fuelprices.gr'
# The base path where the files will be stored
DATA_PATH = pathlib.Path('../var')

# The module logger
logger = logging.getLogger(__name__)


class FuelData(enum.Enum):
    """Enumeration for the different types of fuel data.
    """
    WEEKLY = 'deltia.view',
    DAILY_COUNTRY = 'deltia_d.view',
    DAILY_PREFECTURE = 'deltia_dn.view',

    def __init__(self, page: str):
        """Creates the enum.

        :param page: The page path, relative to the base URL, from which we will fetch the data.
        """
        self.page = page


def fetch_data():
    """Fetch data from the site.
    """
    for fuel_data in FuelData:
        response = requests.get(f"{BASE_URL}/{fuel_data.page}")
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            if link.has_attr('href') and link['href'].startswith('./files'):
                file_link = link['href'].replace(' ', '')
                file_link = re.sub(r'\(\d\)', '', file_link)
                file_link = re.sub(r'-\?+', '', file_link)
                file_path = DATA_PATH / str(fuel_data) / link['href']
                if not file_path.exists():
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_url = f"{BASE_URL}/{file_link}"
                    logger.info(f"Downloading file %s", file_url)
                    with requests.get(file_url, stream=True) as r, file_path.open('wb') as f:
                        r.raise_for_status()
                        shutil.copyfileobj(r.raw, f)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    fetch_data()
