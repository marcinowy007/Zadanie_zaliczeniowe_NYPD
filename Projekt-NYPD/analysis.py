# Tu znajdują się metody do analiz
import pandas as pd


def get_top5_countries_value_per_capita(df, column_name, value_text):
    df[value_text] = df[column_name] / df["Population"]
    df_1 = df.groupby("Country")[value_text].sum().sort_values(ascending=False)
    top5_countries = df_1.head(5)
    top5_countries = top5_countries.index.tolist()
    return top5_countries


def top5_value_per_capita(df, column_name):
    result = df.copy()
    value_text = f"{column_name} per capita"
    top5 = get_top5_countries_value_per_capita(result, column_name, value_text)
    result = result[result["Country"].isin(top5)]
    result = result[["Year", "Country", value_text, column_name]]
    return result


def CO2_change_last10years(df, start_year, end_year):
    df_last10 = df.copy()
    start_year = start_year if end_year-start_year < 10 else end_year-9

    df_last10 = df_last10[(df_last10["Year"] == start_year) | (df_last10["Year"] == end_year)]
    print(f"The analysis of the change in co2 emissions was based on years: {start_year, end_year}")

    df_last10["CO2 emission per capita"] = df_last10["CO2 emission"] / df_last10["Population"]
    rows = []
    for country in df_last10["Country"].unique():
        try:
            start_CO2 = \
                df_last10[(df_last10["Country"] == country) & (df_last10["Year"] == start_year)]["CO2 emission per capita"].item()
            end_CO2 = \
                df_last10[(df_last10["Country"] == country) & (df_last10["Year"] == end_year)]["CO2 emission per capita"].item()
            row = {"Country": country, "Change of CO2 emission per capita": end_CO2-start_CO2}
            rows.append(row)
        except:
            pass
    df_CO2_change = pd.DataFrame(rows)
    df_CO2_change.sort_values("Change of CO2 emission per capita", ascending=False, inplace=True)
    top5_CO2_increase = df_CO2_change.head(5)
    top5_CO2_decrease = df_CO2_change.tail(5)
    return top5_CO2_increase, top5_CO2_decrease


# with open("C:/Marcin Łyżwiński/Studia/Narzędzia python/Zadanie zaliczeniowe - folder/Materiały/product", 'r') as tabelka:
#     tabelka = pd.read_csv(tabelka)
# tabeleczka = top5_value_per_capita(tabelka, "CO2 emission", "CO2 emission")
# pass



