# zad9
name = input("Podaj imię: ")
print(f"Witaj, {name}")
age = int(input("Twój wiek: "))
print(f"Twój wiek to: {age}")
namesArray = []
nameAndLastName = input("Twoje imię i nazwisko: ")
namesArray= nameAndLastName.split(" ")
firstName = namesArray[0]
lastName = namesArray[1]
print(firstName[0],lastName[0])
strText = input("Podaj stringa: ")
print(strText*5)
stringsArr = []
stringsArr.append(input("Pierwszy string: "))
stringsArr.append(input("Drugi string: "))
stringsArr.append((stringsArr[0]+stringsArr[1]))
print(stringsArr)
str1 = input("Pierwszy string ")
str2 = input("Drugi string ")
polowa1 = len(str1) // 2
polowa2 = len(str2) //2
str3 = str1[:polowa1] + str2[:polowa2]
