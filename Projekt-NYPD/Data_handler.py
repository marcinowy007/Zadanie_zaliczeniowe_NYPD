# Ta klasa będzie obsługiwała pliki i tworzyła tabelkę dla każdego pliku z interesującymi danymi.
# Ewentualnie może będzie potem tworzyć jedną tabelkę.

import pandas as pd
from pycountry import countries, historic_countries
from COUNTRY_RENAMING_DICT import COUNTRY_RENAMING_DICT

class Data_handler:

    def __init__(self, GDP_path: str, population_path: str, emissions_path: str, country_renaming_dict=COUNTRY_RENAMING_DICT):
        '''tworzenie tabelek na podstawie podanych ścieżek'''
        with open(GDP_path, 'r') as GDP, open(population_path, 'r') as population, open(emissions_path, 'r') as emissions:
            GDP = pd.read_csv(GDP, skiprows= 4)
            population = pd.read_csv(population, skiprows=4)
            emissions = pd.read_csv(emissions)

        # Określanie lat jakie są dostępne w plikach
        GDP_years = [int(year) for year in GDP.columns if year.isdigit()]
        GDP_start = min(GDP_years)
        GDP_end = max(GDP_years)
        population_years = [int(year) for year in population.columns if year.isdigit()]
        population_start = min(population_years)
        population_end = max(population_years)
        emissions_start = emissions["Year"][0] # Wolę mieć lata w stringach żeby móc je printować użytkownikowi
        emissions_end = emissions["Year"].iloc[-1]
        self.available_years = (max({GDP_start, population_start, emissions_start}), min({GDP_end, population_end, emissions_end}))

        # Formatowanie tabelek z poszczególnych plików, żeby łatwiej było je połączyć oraz określenie nazw państw
        self.country_renaming_dict = country_renaming_dict
        GDP = self.horizontal_pipeline(GDP, "GDP")
        population = self.horizontal_pipeline(population, "Population")
        emissions = self.vertical_pipeline(emissions, "CO\u2082 emission")
        # Łączenie tabelek
        merged_GDP_and_population = pd.merge(GDP, population, on=["Country", "Year"])
        self.product = pd.merge(merged_GDP_and_population, emissions, on=["Country", "Year"])
        self.product.to_csv("C:/Marcin Łyżwiński/Studia/Narzędzia python/Zadanie zaliczeniowe - folder/Materiały/product", index=False)

        # for country in set(self.product["Country"]):
        #     print(country)



    def horizontal_pipeline(self, df, value_name: str):
        '''Used to preprocess data from this website: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD and in the same format'''
        # trzeba sprawdić czy mieści się w latach NIE TRZEBA JUŻ SPRAWDZIŁEŚ
        significant_data = df[["Country Name"]+[str(i) for i in range(int(self.available_years[0]), int(self.available_years[1])+1)]]
        significant_data = significant_data.rename(columns={"Country Name": "Country"})
        significant_data["Country"] = significant_data["Country"].apply(lambda x: self.country_renamer(x))
        melted_data = significant_data.melt(id_vars=["Country"], var_name="Year", value_name=value_name)
        melted_data["Year"] = melted_data["Year"].astype("uint64")
        melted_data = melted_data.dropna(subset=['Country'])
        return melted_data


    def vertical_pipeline(self, df, value_name: str):
        '''Used to preprocess data from this website: https://datahub.io/core/co2-fossil-by-nation and in the same format'''
        # I need specific years
        start = int(self.available_years[0])
        end = int(self.available_years[1])
        significant_data = df.loc[(start <= df["Year"]) & (df["Year"] <= end), ["Year", "Country", "Total"]]
        significant_data.reset_index(drop=True, inplace=True)
        significant_data = significant_data.rename(columns={"Total": value_name})
        vert_dict = self.vert_country_renamer_help(significant_data["Country"])
        significant_data["Country"].replace(vert_dict, inplace=True)
        significant_data = significant_data.dropna(subset=['Country'])
        return significant_data

    def vert_country_renamer_help(self, countries_ls):
        countries_set = set(countries_ls)
        vert_dict = {country: self.country_renamer(country) for country in countries_set}
        # Have to add handwritten dict
        return vert_dict

    def country_renamer(self, country_name):
        try:
            return historic_countries.search_fuzzy(country_name)[0].name
        except:
            try:
                return countries.search_fuzzy(country_name)[0].name
            except:
                try:
                    self.country_renaming_dict[country_name.lower()]
                except:
                    pass

    # def country_renamer(self, country_name):
    #     print(type(country_name))
    #     tekst = countries.search_fuzzy(country_name)[0]
    #     return tekst.name






GDP_path = "Data/GDP.csv"
population_path = "Data/Population.csv"
emissions_path = "Data/fossil-fuel-co2-emissions-by-nation_csv.csv"

Data_handler(GDP_path, population_path, emissions_path)




