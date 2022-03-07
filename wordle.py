import discord
import asyncio
import os
from random import randint
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user: # Bot doesn't respond to it's own message
        return
    if message.content.startswith("-Wordle"): # If user inputs command -Wordle, starts game

        # Picks random word from the word's list
        with open("wordList.txt") as f:
            lines = f.readlines()
        wordSelect = randint(1,len(lines))
        word = lines[wordSelect - 1]
        word = word[:5]
        await message.channel.send("Wordle Initialized:")
        gameOver = False
        strPrint = ""

        # For each guess
        for i in range(6):
            if i > 0: # If it isn't the first guess then tabs for the next guess
                strPrint += "\n"
            await message.channel.send(f"Enter 5 letters (Guess {i + 1}/6):")
            def checkGuess(m): # Checks for 5 letter guess
                return m.author == message.author and len(m.content) == 5
            try:
                guess = await client.wait_for('message', check=checkGuess, timeout=120.0) # Waits for user's guess
            except asyncio.TimeoutError:
                return await message.channel.send(f"Sorry, you took too long it the word was {word}") # Timeout after 2 minutes
                gameOver = True
            if guess.content.upper() == word: # If the user correctly guesses the word
                await message.channel.send(":green_square: :green_square: :green_square: :green_square: :green_square: ")
                await message.channel.send("You are correct!")
                gameOver = True
                break;
            else: # Else colour the letters correctly based on the position
                guessArray = []
                wordArray = []
                colouredWord = [":white_large_square:",":white_large_square:",":white_large_square:",":white_large_square:",":white_large_square:"]
                for x in range(5): # Adds guess to an array
                   guessArray.append(guess.content[x].upper())
                for y in range(5): # Adds word to an array
                   wordArray.append(word[y])
                for n in range(5):
                    # If the guessed letter is in the correct position replace white with green
                    if guessArray[n] == wordArray[n]:
                        colouredWord[n] = ":green_square:"
                        guessArray[n] = None
                        wordArray[n] = None
                for m in range(5):
                    # If the guessed letter is in the word but not correct position and is not already a correctly guessed letter then replace white with yellow
                    if guessArray[m] is not None and guessArray[m] in wordArray:
                        colouredWord[m] = ":yellow_square:"
                        wordArray[wordArray.index(guessArray[m])] = None

                # Adds the squares to strPrint
                strPrint += "".join(colouredWord)
                await message.channel.send(f"{strPrint}")

        # If user runs out of guesses
        if gameOver == False:
            await message.channel.send(f"You ran out of guesses! Too bad, the word was {word}")


@client.event
async def on_ready():
    print ("Ready")

client.run(token)