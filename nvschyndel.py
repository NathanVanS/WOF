from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random
# Should have made a fill word loop
players={0:{"roundtotal":0,"gametotal":5,"name":""},#Players dictionary of  dictionaries
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

dictionary = [] # all the words
turntext = ""
wheellist = [] # wheel spin options 
roundWord = "" # the actual word
blankWord = [] # list of underscores
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""

def readDictionaryFile(): #Done
    global dictionary
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
    file = open(dictionaryloc, "r")
    words = file.read()
    dictionary = list(map(str, words.split()))
    file.close()

def readTurnTxtFile(): #Update the message
    global turntext   
    #read in turn intial turn status "message" from file
    file = open(turntextloc, "r")
    turntext = file.read()
    file.close()
        
def readFinalRoundTxtFile(): #Update the message
    global finalroundtext   
    #read in turn intial turn status "message" from file
    file = open(finalRoundTextLoc, "r")
    finalroundtext = file.read()
    file.close()

def readRoundStatusTxtFile(): #update the message
    global roundstatus
    # read the round status  the Config roundstatusloc file location 
    #read in turn intial turn status "message" from file
    file = open(roundstatusloc, "r")
    roundstatus = file.read()
    file.close()

def readWheelTxtFile(): #Done
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    file = open(wheeltextloc, "r")
    words = file.read()
    wheellist = list(map(str, words.split(",")))
    file.close()
    
def getPlayerInfo(): #done
    global players
    # read in player names from command prompt input
    for i in players:
        players[i]['name'] = input("What is your name?")

def gameSetup(): #Done
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile()
    
def getWord(): #Done 
    #choose random word from dictionary
    #make a list of the word with underscores instead of letters.
    global dictionary

    roundWord = random.choice(dictionary)
    
    for i in roundWord:
        blankWord.append("_")
    return roundWord, blankWord

def wofRoundSetup(): #Done
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    # Return the starting player number (random)
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    blankWord = []
    for i in players:
        players[i]['roundtotal'] = 0
    initPlayer = random.randrange(0,3)
    roundWord, blankWord = getWord()

    return initPlayer

def spinWheel(playerNum): #Done error in that if you dont like your roll you can reroll with a vowel
    global wheellist
    global players
    global vowels
    stillinTurn = True
    # Get random value for wheellist
    # Check for bankrupcy, and take action.
    # Check for lose turn
    # Get amount from wheel if not loose turn or bankruptcy
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
    # Change player round total if they guess right.
    wheelValue = random.choice(wheellist)
    print(f"You got {wheelValue}")
    if wheelValue == 'BANKRUPT':
        players[playerNum]['roundtotal'] = 0
        stillinTurn = False
        print("Bummer")
    if wheelValue == 'LOSE A TURN':
        stillinTurn = False
        print("No more turn for you!")
    elif stillinTurn:
        stillinTurn = guessletter(input("Guess a letter."), playerNum)
        if stillinTurn:
            players[playerNum]['roundtotal'] += int(wheelValue) 
            #players[playerNum]['roundtotal'] = count * int(wheelValue)
            # stillinTurn, count = guessletter() 

    return stillinTurn

def guessletter(letter, playerNum): #Done
    global players
    global blankWord
    global vowels
    global roundWord
    index = -1
    goodGuess = False
    # count = 0
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore 
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    # ensure letter is a consonate.
    if letter in vowels:
        print("You picked a vowel.  Try again.")
        wofTurn(playerNum)
    else:
        for i in roundWord:
            index += 1
            if i == letter:
                blankWord[index] = letter
                goodGuess = True
                #count += 1
    
    return goodGuess#,count #count is the number of times it was correct? which doesnt matter according to the rubrick

def buyVowel(letter, playerNum): #Done 
    global players
    global vowels

    goodGuess = False
    
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    if letter not in vowels:
        goodGuess = buyVowel(input("VOWELS. Try again"), playerNum)
        return goodGuess
    if players[playerNum]['roundtotal'] < 250:
        print(f"{players[playerNum]['name']} honey, you cant afford a vowel.  MMM MMMMM")
        guessletter(input("Guess a letter that isnt a vowel."), playerNum) 
    else:
        players[playerNum]['roundtotal'] -= vowelcost
        index = -1
        for i in roundWord:
            index += 1
            if i == letter:
                blankWord[index] = letter
                goodGuess = True
    
    return goodGuess      
        
def guessWord(playerNum): #Done
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish) 
    wordGuess = input(f"What is the word {players[playerNum]['name']}?")
    if wordGuess.lower() == roundWord:
        print("That is correct!")
        for i in wordGuess:
            index = -1
            for x in roundWord:
                index += 1
                if i == x:
                    blankWord[index] = i
    else:
        print("Unfortunately, no.")
        
    return False
    
def wofTurn(playerNum):  #Done needs checking
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    print(turntext.format(players[playerNum]['name']))
        
    for unimportantNumber, p_info in players.items():
        for key in p_info:
            print(key + ':', p_info[key])
    stillinTurn = True
    while stillinTurn:
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word

        choice = input("Would you like to (S)pin the wheel, (B)uy vowel, or G(uess) the word.")  
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(input("Pick a vowel homes"), playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option") 

        if "_" not in blankWord:
            stillinTurn = False
    return stillinTurn
    
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     

def wofRound(roundNumber): #Done needs checking
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    thisRound = True
    samePlayer = True

    print(roundstatus.format(roundNumber+1))
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    while thisRound == True:
        samePlayer =  True
        while samePlayer == True:
            samePlayer = wofTurn(initPlayer)
            if "_" not in blankWord:
                thisRound = False
                players[initPlayer]['gametotal'] += players[initPlayer]['roundtotal']
            if initPlayer < 2:
                initPlayer += 1
            else:
                initPlayer = 0 
        
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    finalRoundList = ["r","s","t","l","n"] # no vowels
    winplayer = 0
    amount = finalprize
    
    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    # If they do, add finalprize and gametotal and print out that the player won 
    currentHighest = 0
    for i in players:
        if players[i]['gametotal'] > currentHighest:
            currentHighest = players[i]['gametotal']
            winplayer = i

    print(finalroundtext.format(players[winplayer]['name']))
    roundWord, blankWord = getWord()
    players[winplayer]['roundtotal'] = 500
    for i in finalRoundList:
        guessletter(i, winplayer)
    buyVowel("e", winplayer) # cost doesnt matter since its round, but they needs money
    print(f'The revealed letters are! {blankWord}')
    for x in range(0,3):
        guessletter(input("Pick a consonant."), winplayer)
    buyVowel(input("Pick one last vowel."), winplayer)
    print(blankWord)
    if guessWord(winplayer) is False:
        print(f"Your total was {players[winplayer]['gametotal']}.  Amazing you win, uh? {amount}")

def main():
    gameSetup()    
    for initPlayer in range(0,maxrounds):
        if initPlayer in [0,1]:
            wofRound(initPlayer)
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()