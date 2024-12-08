# z3
def greetUser(język="polski",username="Użytkowniku"):
     match język:
         case "angielski":
            print(f"Hello,{username}")
         case "niemiecki":
             print(f"Guten Morgen, {username}")
         case _ : \
             print(f"Witaj, {username}")