# z3
adressArr = [] 
apartamentNum = 1
buildingNum =1
amountOfApartaments = 10
amountOfBuildings = 5
dzielnice = ("Jagodowa","Lipowa","Kwiatowa","Kasztanowa","Polna")
for street in dzielnice:
    while(buildingNum<=amountOfBuildings):
        adressArr.append(f"{street} {buildingNum}/{apartamentNum}" )
        apartamentNum += 1
        if(apartamentNum==amountOfApartaments+1):
            buildingNum += 1
            apartamentNum=1


    apartamentNum =1
    buildingNum =1
print(adressArr)