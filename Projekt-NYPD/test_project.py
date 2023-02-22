import pytest
import pandas as pd
from pycountry import countries, historic_countries
from COUNTRY_RENAMING_DICT import COUNTRY_RENAMING_DICT
from Data_handler import Data_handler
from main import main

parser = argparse.ArgumentParser(description="required files paths")
parser.add_argument("GDP_path", type=str, help="Provide path for GDP data")
parser.add_argument("population_path", type=str, help="Provide path for population data")
parser.add_argument("emissions_path", type=str, help="Provide path for emissions data")
args = parser.parse_args()

GDP_path = args[0]
population_path = args[1]
emissions_path = args[2]


# Test the initialization of the class
def test_initialization():
    data_handler = Data_handler(GDP_path, population_path, emissions_path)
    assert isinstance(data_handler.available_years, tuple)
    assert isinstance(data_handler.country_renaming_dict, dict)
    assert isinstance(data_handler.product, pd.DataFrame)


def test_country_renamer():
    data_handler = Data_handler(GDP_path, population_path, emissions_path)
    assert data_handler.country_renamer("UsA") == "United States"
    assert data_handler.country_renamer("china (mainland)") == "China"
    assert data_handler.country_renamer("ST. lucia") == "Saint Lucia"
