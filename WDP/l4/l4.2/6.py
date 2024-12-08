# 6
import math

def calculateTriangleArea(a, b, c):
    try:
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Boki muszą być dodatnie.")
        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return area
    except ValueError as e:
        return str(e)

a = float(input("Podaj bok a: "))
b = float(input("Podaj bok b: "))
c = float(input("Podaj bok c: "))
area = calculateTriangleArea(a, b, c)
print(f"Pole trójkąta wynosi: {area}")