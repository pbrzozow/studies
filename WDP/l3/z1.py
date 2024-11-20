# z1
paliwo = 100
paliwo_zużyte_na_s = 10
czas = 0
while (paliwo>0):
    print(f"Ilość paliwa {paliwo} czas:{czas}")
    paliwo -=paliwo_zużyte_na_s
    czas+=1
print("Koniec lotu")