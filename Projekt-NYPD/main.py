import pandas as pd
# Tu będzie wywoływanie wszystkiego i wczytywanie danych ( a przynajmniej w wersji końcowej)

def co2_per_capita_analysis(df):
    df["CO2 emission per capita"] = df["CO2 emission"] / df["Population"]
    co2_per_capita_by_country = df.groupby("Country")["CO2 emission per capita"].sum().sort_values(ascending=False)
    top5_countries = co2_per_capita_by_country[:5]
    top5_countries = top5_countries.index.tolist()
    print(top5_countries)
    pass


def main():
    # Tu trzeba użyć DataHandlera
    with open("C:/Marcin Łyżwiński/Studia/Narzędzia python/Zadanie zaliczeniowe - folder/Materiały/product", 'r') as tabelka:
        tabelka = pd.read_csv(tabelka)
    co2_per_capita_analysis(tabelka)

main()
