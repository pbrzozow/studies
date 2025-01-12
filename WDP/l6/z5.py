import numpy as np

macierz = np.random.rand(5, 5)

najwiekszy = np.max(macierz)
najmniejszy = np.min(macierz)
najwieksze_wiersze = np.max(macierz, axis=1)
najwieksze_kolumny = np.max(macierz, axis=0)
suma_wierszy = np.sum(macierz, axis=1)

print(suma_wierszy)