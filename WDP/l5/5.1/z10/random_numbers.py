import random as rd
import math
minimum_przedziału = int(input("Dolna wartość przedziału"))
maksimum_przedziału = int(input("Górna wartość przedziału"))

krotka =  tuple(rd.uniform(minimum_przedziału, maksimum_przedziału) for _ in range(10))

result =1
for i in krotka:
    result*=i

result = math.pow(result,(1/len(krotka)))
print(result)