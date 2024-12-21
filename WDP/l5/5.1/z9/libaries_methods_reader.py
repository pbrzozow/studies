# Wyświetl wszystkie nazwy funkcji zawartych w modułach: math, tuple, keyword
import math
import keyword
import inspect

def getMembers(module):
    return inspect.getmembers(module)

print(getMembers(math),getMembers(keyword),getMembers(tuple))