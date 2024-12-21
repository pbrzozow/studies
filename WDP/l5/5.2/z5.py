import pandas as pd


data = {
    'Nr_albumu': [1, 2, 3, 4, 5],
    'Imię': ['Anna', 'Jan', 'Katarzyna', 'Tomasz', 'Michał'],
    'Nazwisko': ['Kowalska', 'Nowak', 'Wiśniewska', 'Kaczmarek', 'Zieliński'],
    'Ocena': [4.5, 3.0, 5.0, 4.0, 2.5],
    'Wiek': [22, 21, 24, 23, 25]
}


df = pd.DataFrame(data)

students_grades = df[df['Ocena'] > 4]
print("Studenci z oceną większą niż 4:")
print(students_grades)

sorted_by_age = df.sort_values(by='Wiek')
print("Studenci według wieku:")
print(sorted_by_age)

average_age_by_grade = df.groupby('Ocena')['Wiek'].mean()
print("Średnia wieku w każdej grupie ocen:")
print(average_age_by_grade)


correction_data = {
    'Nr_albumu': [2, 5],
    'Nowa Ocena': [4.0, 3.5]
}


correction_df = pd.DataFrame(correction_data)

merged_df = pd.merge(df, correction_df, on='Nr_albumu', how='left')

print("Dane studentów po poprawie ocen:")
print(merged_df)


merged_df.to_csv('studenci_z_poprawkami.csv', index=False)
print("Dane zapisane")


loaded_df = pd.read_csv('studenci_z_poprawkami.csv')

print("Wczytane dane z pliku :")
print(loaded_df)


new_student = {'Nr_albumu': 6, 'Imię': 'Piotr', 'Nazwisko': 'Nowak', 'Ocena': 4.8, 'Wiek': 22}


df = df._append(new_student, ignore_index=True)

print("Dane studentów po dodaniu nowego studenta:")
print(df)

unique_grades = df['Ocena'].unique()
print("Unikalne wartości w kolumnie z ocenami:")
print(unique_grades)

count_grade_5 = df[df['Ocena'] == 5].shape[0]
print("Liczba studentów z oceną równą 5:")
print(count_grade_5)
