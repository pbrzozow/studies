import numpy as np

macierz = np.random.randint(0, 51, (5, 5))

print(macierz)

wieksze_niz_20 = macierz[macierz > 20]
liczba_elementow_wiekszych_niz_20 = len(wieksze_niz_20)

print("Elementy większe niż 20:")
print(wieksze_niz_20)
print("Liczba elementów większych niż 20:", liczba_elementow_wiekszych_niz_20)

srednia = np.mean(macierz)
print("Średnia wartość ", srednia)