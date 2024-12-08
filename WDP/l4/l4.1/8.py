# z8
stopnie = ("Szeregowy",
 "Kapral",
 "Sierżancie",
 "Porucznik",
 "Kapitan",
 "Major",
 "Pułkownik")
ilosc_stopni = len(stopnie)
major_index = stopnie.index("Major")
pulkownik_wystepowanie = stopnie.__contains__("Pułkownik")
print(ilosc_stopni,major_index,pulkownik_wystepowanie)