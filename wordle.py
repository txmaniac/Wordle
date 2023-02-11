from rich.console import Console
from random import choice
from collections import Counter
import time

color_codes = {
    1: "bold white on yellow",
    2: "white on #666666",
    3: "bold white on green"
}

def find_idx(str, ch):
    return [i for i, c in enumerate(str) if c == ch]

def validate(word, guessed_word):
    # n = len(word)
    # result = []
    # for i in range(n):
    #     if word[i] != guessed_word[i]:
    #         indexes = find_idx(word, guessed_word[i])
    #         guess_indexes = find_idx(guessed_word, guessed_word[i])

    #         print(indexes)
    #         print(guess_indexes)

    #         if len(indexes) != len(guess_indexes) and len(indexes) > 0 and len(guess_indexes) > 0:

    #             for index in guess_indexes:
    #                 if word[index] != guess_indexes[index]: 
    #                     result.append(f"[{color_codes[2]}]{guessed_word[i]}[/]")

    #         elif guessed_word[i] in word:
    #             result.append(f"[{color_codes[1]}]{guessed_word[i]}[/]")
                
    #         else:
    #             result.append(f"[{color_codes[2]}]{guessed_word[i]}[/]")

    #     else:
    #         result.append(f"[{color_codes[3]}]{guessed_word[i]}[/]")
    
    # correct chars with indexes
    i = 0
    char_counts = Counter(word)
    
    correct_indexes = []
    for ch, gch in zip(word, guessed_word):
        if ch == gch:
            correct_indexes.append(i)
            char_counts[ch] -= 1
        i+=1

    # misplaced chars with indexes
    misplaced_indexes = []

    for i in range(0,len(guessed_word)):
        if guessed_word[i] in word and i not in correct_indexes and char_counts[guessed_word[i]] > 0:
            misplaced_indexes.append(i)
            char_counts[guessed_word[i]] -= 1

    result = ["TEXT"] * len(word)

    remaining_indexes = []

    # remaining chars with indexes
    for i in range(len(word)):
        if i not in correct_indexes and i not in misplaced_indexes:
            remaining_indexes.append(i)

    for ch in misplaced_indexes:
        result[ch] = f"[{color_codes[1]}]{guessed_word[ch]}[/]"

    for ch in remaining_indexes:
        result[ch] = f"[{color_codes[2]}]{guessed_word[ch]}[/]"

    for ch in correct_indexes:
        result[ch] = f"[{color_codes[3]}]{guessed_word[ch]}[/]"
    return result

def getWord():
    my_file = open("./sgb-words.txt", "r")
    data = my_file.read()
    word= choice(data.split("\n")).upper()
    my_file.close()

    return word

def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")

def game_over(guesses, word):
    refresh_page(headline="Game Over")
    showGuesses(guesses)
    print(word)

def game_won(result):
    refresh_page(headline="Game WON")
    showGuesses(result)

def showGuesses(result):
    for res in result:
        console.print("".join(res), justify="center")

if __name__ == "__main__":

    console = Console()
    console.print("Hello, [bold red]Rich[/] :SNAKE:")
    word = getWord()

    # number of tries is 6 words
    num_of_tries = 6
    results = []

    while True and num_of_tries:

        refresh_page(headline=f"Guess {6 - num_of_tries + 1}")
        showGuesses(results)

        guessed_word = console.input("\nGuess word: ").upper()

        if(len(guessed_word) < 5):
            console.print("Enter 5 lettered words only")
            time.sleep(1)
            continue

        if word == guessed_word:
            result = [f"[{color_codes[3]}]{guessed_word[ch]}[/]" for ch in range(len(guessed_word))]
            results.append(result)
            game_won(results)
            num_of_tries-=1
            break
        
        else:    
            results.append(validate(word, guessed_word))
            num_of_tries -=1

    if num_of_tries == 0 and word == guessed_word:
        result = [f"[{color_codes[3]}]{guessed_word[ch]}[/]" for ch in range(len(guessed_word))]
        results.append(result)
        game_won(results)

    elif num_of_tries == 0 and word != guessed_word:
        game_over(results, word)