# z2
def czy_pierwsza(liczba):
    if liczba < 2:
        return False
    for i in range(2, liczba):
        if liczba % i == 0:
            return False
    return True

liczba = 2
liczby_pierwsze = []
znalezione = 0

while znalezione < 10:
    if czy_pierwsza(liczba):
        liczby_pierwsze.append(liczba)
        znalezione += 1
    liczba += 1

print(liczby_pierwsze)
