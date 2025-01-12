import numpy as np

macierz = np.zeros((5, 5),dtype=int)

macierz[0, :] = 1
macierz[-1, :] = 1
macierz[:, 0] = 1
macierz[:, -1] = 1

print(macierz)
macierz = np.where(macierz == 0, 1, 0)

print("Zmieniona macierz:")
print(macierz)