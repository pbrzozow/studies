# 7
def power(a, n):
    if n == 0:
        return 1
    else:
        return a * power(a, n - 1)

a = float(input("Podaj podstawę a: "))
n = int(input("Podaj wykładnik n: "))
print(f"{a} do potęgi {n} to {power(a, n)}.")