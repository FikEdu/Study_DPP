#def is_palindrome(word):
#    drow = ""
#    for i in range(len(word)):
#        drow += word[len(word)-i-1]
#    return word == drow
#
#print(is_palindrome("skala"))

#def fibonacci(liczba):
#    if liczba == 1:
#        return 1
#    elif liczba == 0:
#        return 0
#    elif liczba > 1:
#        return fibonacci(liczba-1) + fibonacci(liczba-2)
#
#print(fibonacci(20))

#def count_vowels(text: str):
#    vowels_amt = 0
#    for letter in text.lower():
#        if letter in ('a', 'e', 'i', 'o', 'u', 'y'):
#            vowels_amt += 1
#    return vowels_amt
#
#print("ilosc samoglosek to: ", end = "")
#print(count_vowels('skala'))

def calculate_discount(price: float, discount: float):
    if discount < 0 or discount > 1:
        raise ValueError
    return price * (1-discount)

print(calculate_discount(100, 0.2))