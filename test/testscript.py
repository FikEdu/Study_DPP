def is_palindrome(word):
    drow = ""
    for i in range(len(word)):
        drow += word[len(word)-i-1]
    return word == drow

print(is_palindrome("skala"))