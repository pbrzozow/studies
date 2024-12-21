
import pandas as pd
df =pd.read_csv('WDP/l5/5.2/demografia.csv',decimal='.',na_values=['NA', 'n/a', 'NaN'])
    
country_with_max_growth_2022=df['KRAJE'].iloc[df['2022'].idxmax(skipna=True)]
print(f"Kraj z największym przyrostem w 2022 to: {country_with_max_growth_2022}")
# 
# 
# ta linijka była problematyczna
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')


df_without_countries = df.drop(columns=['KRAJE'])
max_growth_value = df_without_countries.max().max()
year_with_max_growth = df_without_countries.max().idxmax()
country_index_with_max_growth = df[year_with_max_growth].idxmax()

country_with_max_growth = df.loc[country_index_with_max_growth, 'KRAJE']

print(f"Największy przyrost ludności wyniósł {max_growth_value}")
print(f"Rok: {year_with_max_growth}")
print(f"Kraj: {country_with_max_growth}")



# print(max_value)




