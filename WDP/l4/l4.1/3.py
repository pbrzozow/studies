# z3
name = input('Enter the name: ')
print(f'Witaj, {name}!')
age = int(input('Enter the name: '))
print(f'Twój wiek to: , {age}!')
firstAndLastName = input('Podaj imię i nazwisko: ').split(' ')
initials = firstAndLastName[0][:1]+firstAndLastName[1][:1]
print(initials)
strToPrint = input('Podaj łańcuch: ')
print(strToPrint*5)
firstVal = input('Pierwszy łańcuch: ')
secondVal = input('Drugi łańcuch: ')
compositeVal = firstVal+secondVal
print(compositeVal)
customCompositeVal = firstVal[:len(firstVal)//2]+secondVal[:len(secondVal)//2]
print(customCompositeVal)
