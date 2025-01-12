import numpy as np

wagi=np.array([128,64, 32 ,16, 8 ,4 ,2 ,1])
wartosci = np.array([0,0,0,0,0,1,1,1])
sum= 0
current_index = 0
for i in wartosci:
    if wartosci[current_index]==1:
        sum+=wagi[current_index]
    current_index+=1
print(sum)