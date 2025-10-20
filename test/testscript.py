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

#def calculate_discount(price: float, discount: float):
#    if discount < 0 or discount > 1:
#        raise ValueError
#    return price * (1-discount)
#
#print(calculate_discount(100, 0.2))

#def flatten_list(nested_list: list):
#    mem = []
#    for i in range(len(nested_list)):
#        if type(nested_list[i]) == list:
#            mem = mem + flatten_list(nested_list[i])
#        else:
#            mem = mem + [nested_list[i]]
#    return mem

#my_list = [1, [2, 3], [4, [5]]]

#print(flatten_list(my_list))

def word_frequencies(text: str):
    word_count = {}
    for word in text.lower().strip(',.').split():
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] = word_count[word] + 1
    return word_count

print(word_frequencies('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'))