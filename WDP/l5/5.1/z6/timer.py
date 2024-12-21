import time

seconds = int(input("Podaj czas do odliczenia: "))
while seconds > 0:
    print(f"Pozostało {seconds} sekund")
    time.sleep(1)
    seconds -= 1
print("Czas minął!")