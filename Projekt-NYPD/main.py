# Tu będzie wywoływanie wszystkiego i wczytywanie danych ( a przynajmniej w wersji końcowej)
import pandas as pd
from analysis import *
from Data_handler import Data_handler
import argparse


def main():

    parser = argparse.ArgumentParser(description="required files paths")
    parser.add_argument("GDP_path", type=str, help="Provide path for GDP data")
    parser.add_argument("population_path", type=str, help="Provide path for population data")
    parser.add_argument("emissions_path", type=str, help="Provide path for emissions data")
    args = parser.parse_args()
    # Tu trzeba użyć DataHandlera
    GDP_path = "Data/GDP.csv"
    population_path = "Data/Population.csv"
    emissions_path = "Data/fossil-fuel-co2-emissions-by-nation_csv.csv"
    data_handler = Data_handler(args.GDP_path, args.population_path, args.emissions_path)
    # data_handler = Data_handler(GDP_path, population_path, emissions_path)
    df_processed = data_handler.product
    start_year, end_year = data_handler.available_years
    # start_year = 1960
    # end_year = 2014
    # with open("C:/Marcin Łyżwiński/Studia/Narzędzia python/Zadanie zaliczeniowe - folder/Materiały/product", 'r') as tabelka:
    #     tabelka = pd.read_csv(tabelka)
    # df_processed = tabelka
    top5_CO2_per_capita = top5_value_per_capita(df_processed, "CO2 emission")
    top5_GDP_per_capita = top5_value_per_capita(df_processed, "GDP")
    top5_CO2_increase, top5_CO2_decrease = CO2_change_last10years(df_processed, start_year, end_year)
    return [top5_CO2_per_capita,
            top5_GDP_per_capita,
            top5_CO2_increase,
            top5_CO2_decrease]



main()

# "Data/GDP.csv" "Data/Population.csv" "Data/fossil-fuel-co2-emissions-by-nation_csv.csv"
