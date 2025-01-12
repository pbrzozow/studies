import matplotlib.pyplot as plt


kategorie = ['kasza manna', 'kukurydza', 'rowery', 'banan']
udzial = [1, 3, 19, 2]
plt.pie(udzial, labels=kategorie,
autopct='%1.f%%', startangle=90,
colors=['skyblue', 'lightgreen',
'black', 'red'])
plt.title('Udział w kategoriach')
plt.show()