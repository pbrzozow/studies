# z5
maxNum = 80
currentNum = maxNum
numbers = []
step = 4
while(currentNum>=0):
    numbers.append(currentNum)
    currentNum-=step
print(numbers)