import random
# z1
a1 = 1 + 2
#1 <class 'int'>
a2=1 + 4
#2 <class 'int'>
a3= 3 / 2
# 3 <class 'float'>
a4= 4 / 2
# 4 <class 'float'>
a5= 3 // 2
# 5 <class 'int'>

a6= -3 // 2
# 6 <class 'int'>
a7= 11 % 2
# 7 <class 'int'>
a8= 2 ** 10
# 8 <class 'int'>

a9= 8 ** (1/3)
# 9 <class 'float'>
print(type(a1),type(a2),type(a3),type(a4),type(a5),type(a6),type(a7),type(a8),type(a9))
#z2
uczelnia ='Studiuję na WSIiZ'
print(uczelnia)
# z3
imię = 'Jan'
wiek = 20
wzrost = 178
print(f"Nazywam się {imię} i mam {wiek} lat. Mój wzrost to {wzrost} cm.")
# z4
Cena =39.99 
Rabat = 0.2
print('{0:.2f}'.format(Cena*(1-Rabat)),'PLN')
#31.99 PLN
# z5
a=float(input('Podaj długość pierwszego boku '))
b=float(input('Podaj długość drugiego boku '))
print('Pole=',a*b,' Obwód=',2*a+2*b)
# z6
s1=float(input('Podaj drogę '))
avg1=float(input('Podaj spalanie (l/100km) '))
fuelPrice1= 6.5
fuelPredict1 = s1/100*avg1
print(f'Droga {s1}km spalanie {fuelPredict1}l koszt podróży to {fuelPredict1*fuelPrice1}zł')
# z6a
s2=random.randint(1,1000)
avg2=float(input('Podaj spalanie (l/100km) '))
fuelPrice2= float(input('Cena paliwa '))
fuelPredict2 ='{0:.2f}'.format(s2/100*avg2) 
print(f'Droga {s2}km spalanie {fuelPredict2}l koszt podróży to {fuelPredict2*fuelPrice2}zł')

