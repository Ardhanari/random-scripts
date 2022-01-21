import re
import time # why tho

originalPhrase = input("Feed me a sentence! \n").lower()

print("\nChosen sentence: " + originalPhrase)
print("Obscuring...")
time.sleep(1) # because I can >:)

# obscure the letters
downWithTheLetters = re.sub(r'[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]', "-", originalPhrase)
# but keep the spaces
andSpacesToo = re.sub(r'\s', "/", downWithTheLetters)

print("\nObsured phrase: " + andSpacesToo)

lettersUsed = input("\nGive me letters that were used!\n")
lettersLower = lettersUsed.lower()
lettersInput = list()

for letter in lettersLower: 
        if letter != ' ': 
            lettersInput.append(letter) 

print(lettersInput)

listOfLetters = list(lettersInput)
lettersFound = list()
lettersNotFound = list()

for i in range(len(listOfLetters)):
    if listOfLetters[i] in originalPhrase: 
        lettersFound.append(listOfLetters[i])
    else:
        lettersNotFound.append(listOfLetters[i])

# print(lettersFound) 
# print(lettersNotFound)

# for loop because at 3:30 am regex breaks my brain
for i in range(len(originalPhrase)):
    # obscures letters that weren't chosen
    if originalPhrase[i] not in listOfLetters and originalPhrase[i] in r'[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZżźćńółęąśŻŹĆĄŚĘŁÓŃ]':
        originalPhrase = re.sub(originalPhrase[i], "-", originalPhrase)
    # leaves spaces alone
    elif originalPhrase[i] == " ":
        originalPhrase = re.sub(originalPhrase[i], "/", originalPhrase)

# amend letters lists for better readability
# make it alphabetic
lettersFound.sort(key=str)
lettersNotFound.sort(key=str)

# join into a clear string
separator = " "
lettersFound2 = separator.join(lettersFound)
lettersNotFound2 = separator.join(lettersNotFound)

  
result = '''\nResults: 
    Obscured phrase: %s
    Solved phrase: %s
    Letters used: %s
    Letters not in the phrase: %s
        ''' % (str(andSpacesToo), str(originalPhrase), str(lettersFound2), str(lettersNotFound2))

print(result)
