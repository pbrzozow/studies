# 5
def calculateBmi(weight, height):
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        category = "niedowaga"
    elif 18.5 <= bmi <= 24.9:
        category = "pożądana masa ciała"
    elif 25 <= bmi <= 29.9:
        category = "nadwaga"
    else:
        if 30 <= bmi <= 34.9:
            category = "otyłość I stopnia"
        elif 35 <= bmi <= 39.9:
            category = "otyłość II stopnia"
        else:
            category = "otyłość III stopnia"
    return bmi, category

weight = float(input("Podaj wagę w kilogramach: "))
height = float(input("Podaj wzrost w metrach: "))
bmi, category = calculateBmi(weight, height)
print(f"Twoje BMI to {bmi:.2f} i znajduje się w kategorii: {category}.")