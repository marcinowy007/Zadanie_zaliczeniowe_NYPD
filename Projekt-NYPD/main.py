import pandas as pd
from analysis import top5_value_per_capita, CO2_change_last10years
from Data_handler import Data_handler
import argparse


def main():
    # Wczytywanie argumentów z wiersza poleceń
    parser = argparse.ArgumentParser(description="required files paths")
    parser.add_argument("GDP_path", type=str, help="Provide path for GDP data")
    parser.add_argument("population_path", type=str, help="Provide path for population data")
    parser.add_argument("emissions_path", type=str, help="Provide path for emissions data")
    args = parser.parse_args()
    # Obiekt data_handler procesuje podane dane i tworzy jedną spójną tabelkę
    data_handler = Data_handler(args.GDP_path, args.population_path, args.emissions_path)
    df_processed = data_handler.product
    start_year, end_year = data_handler.available_years
    # Metody do analiz
    top5_CO2_per_capita = top5_value_per_capita(df_processed, "CO2 emission")
    top5_GDP_per_capita = top5_value_per_capita(df_processed, "GDP")
    top5_CO2_increase, top5_CO2_decrease = CO2_change_last10years(df_processed, start_year, end_year)

    # Nie do końca wiedziałem czy kod ma zwracać data frame'y czy zapisywać jako csv, czy też jeszcze coś innego
    # dlatego poniżej zakomentowałem opcję z zapisem do csv
    # top5_CO2_per_capita.to_csv('top5_CO2_per_capita.csv', index=False)
    # top5_GDP_per_capita.to_csv('top5_GDP_per_capita.csv', index=False)
    # top5_CO2_increase.to_csv('top5_CO2_increase.csv', index=False)
    # top5_CO2_decrease.to_csv('top5_CO2_decrease.csv', index=False)

    return [top5_CO2_per_capita,
            top5_GDP_per_capita,
            top5_CO2_increase,
            top5_CO2_decrease]


main()


