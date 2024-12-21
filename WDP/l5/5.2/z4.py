import pandas as pd

data = {
    'ID': [1, 2, 3, 4, 5],
    'Imie': ['Anna', 'Jan', 'Katarzyna', 'Tomasz', 'Michał'],
    'Nazwisko': ['Kowalska', 'Nowak', 'Wiśniewska', 'Kaczmarek', 'Zieliński'],
    'Stanowisko': ['Manager', 'Programista', 'Konsultant', 'Programista', 'Manager'],
    'Wiek': [35, 28, 40, 30, 45],
    'Pensja': [8000, 4500, 6000, 5500, 7000]
}

df = pd.DataFrame(data)

above_5000_salary = df[df['Pensja'] > 5000]
print("Pracownicy z pensją większą niż 5000")
print(above_5000_salary)

sorted_age = df.sort_values(by='Wiek')
print("Pracownicy według wieku")
print(sorted_age)

grouped_by_position = df.groupby('Stanowisko')['Pensja'].mean()
print("Średnia pensja według zawodu")
print(grouped_by_position)


promotion = {
    'ID': [2, 4],
    'Nowe Stanowisko': ['Senior Programista', 'Senior Programista']
}


promotion_df = pd.DataFrame(promotion)

complete_df = pd.merge(df, promotion_df, on='ID', how='left')

print("Zaktualizowane dane")
print(complete_df)


complete_df.to_csv('pracownicy_z_awansami.csv', index=False)

loaded_df = pd.read_csv('pracownicy_z_awansami.csv')
print('Ostateczna')
print(loaded_df)


