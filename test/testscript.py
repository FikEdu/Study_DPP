#def is_palindrome(word):
#    drow = ""
#    for i in range(len(word)):
#        drow += word[len(word)-i-1]
#    return word == drow
#
#print(is_palindrome("skala"))

def fibonacci(liczba):
    if liczba == 1:
        return 1
    elif liczba == 0:
        return 0
    elif liczba > 1:
        return fibonacci(liczba-1) + fibonacci(liczba-2)

print(fibonacci(20))