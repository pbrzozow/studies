import random
numbers =[]
for i in range(49):
    numbers.append(i+1)
winning_numbers=random.sample(numbers,6)
print("Numery wygrane: ",winning_numbers)