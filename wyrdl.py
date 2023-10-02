import contextlib
import pathlib
import random
from string import ascii_letters, ascii_uppercase

#rich is a third party library that can be used for styling and needs installation
from rich.console import Console
from rich.theme import Theme

NUM_LETTERS = 5
NUM_GUESSES = 6
 #__file__ contains the path to this current file. parent gives the parent dir.
WORDS_PATH = pathlib.Path(__file__).parent /"wordlist.txt"

console = Console(width=100, theme= Theme({"warning": "red on yellow"}))
#--------------------------------------------------------------------------------------
def refresh_page(headline):
    console.clear()
    console.rule(f"[bold purple]:sparkles: {headline} :sparkles:[/] \n")

#-----------------------------------------------------------------------------------------
#use a file to pick a random word as the wordle word to be guessed
def get_random_word(wordlist):

    #create a list of words from wordlist file
    #check that the list contains at least one word. Walrus operator := does the assignment as part of an expression
    #the list of words is assigned to 'words', but also used in the if test to make sure its not empty i.e. if words:

    if words := [
            #convert all to uppercase
            word.upper()
            for word in wordlist
            #filter for words of length NUM_LETTERS and ascii letters (a-z) only
            if len(word) == NUM_LETTERS and all(letter in ascii_letters for letter in word)
    ]: 
        #randomly choose a word from the words list
        return random.choice(words)
    #if the list of words is empty i.e. if words fails
    else: 
        console.print("No words of length {NUM_LETTERS} in the word list", style= "warning")
        #end the program by raising systemexit
        raise SystemExit()

#----------------------------------------------------------------------------------------------------
def show_guesses(guesses, word):

    #dictionary to keep track of letter status so users can see that at a glance
    letter_status = {letter: letter for letter in ascii_uppercase}
    
    for guess in guesses:
        styled_guess = []
        #style letters based on whether they are correct, misplaced or wrong
        #compare letter by letter between a guess and the chosen word
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            #misplaced letter
            elif letter in word:
                style = "bold white on yellow"
            #incorrect letters
            elif letter in ascii_letters:
                style = "bold white on #666666"
            else:
                style = "dim"
            styled_guess.append(f" [{style}] {letter} [/]")
            if letter != "_":
                letter_status[letter] = f'[{style}] {letter} [/]'
           
        console.print("".join(styled_guess), justify ="center")
    console.print("\n" + "".join(letter_status.values()), justify="center")

#----------------------------------------------------------------------------
def game_over(guesses,word, guessed_correctly):
    refresh_page(headline="Game Over")
    show_guesses(guesses, word)

    if guessed_correctly:
        console.print(f"\n:trophy: [bold white on green] Correct, the word is {word}! [/] :trophy:")
    else:
        console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")

#------------------------------------------------------------------------------
def guess_word(previous_guesses):
    #console.input is a from the rich library, used here for consistency
    guess = console.input("\nGuess word: ").upper()

    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}!", style="warning")
        return guess_word(previous_guesses)

    if len(guess) != NUM_LETTERS:
        console.print(f"Your guess must be {NUM_LETTERS} letters.", style="warning")
        return guess_word(previous_guesses)
    
    #use the walrus operator below to assign an invalid letter to 'invalid'
    if any ((invalid := letter) not in ascii_letters for letter in guess):
        console.print(f"Invalid letter: '{invalid}'. Please use English letters.", style= "warning")
        return guess_word(previous_guesses)

    
    return guess

#------------------------------------------------------------------------------

def main():
    #pre-process
    #read the words from the wordlist file
    
    word = get_random_word(WORDS_PATH.read_text(encoding="utf-8").split("\n"))
    
    #guesses is a list of NUM_GUESSES items, each containing _ _ _ _ _ for a NUM_LETTERS guess
    guesses = ["_" * NUM_LETTERS] * NUM_GUESSES

    #Process(main loop)
    #if a keyboard interrupt i.e. ctrl c is raised by the user inside this loop
    #control is passed outside the loop and game over is called
    #the game will end after displaying the word to the user
    with contextlib.suppress(KeyboardInterrupt):
        #take a guess from the user, store it in guesses. allow up to 6 guesses
        for i in range(NUM_GUESSES):        
            #refresh page will clear the screen of all prev guesses
            refresh_page(headline=f"Guess {i+1}")
            print(word)
            show_guesses(guesses, word)

            #send prev guesses to guess_word by only including guesses that have already been filled in
            guesses[i] = guess_word(previous_guesses=guesses[:i])

            if guesses[i] == word:
                break
            
    #post process
    game_over(guesses, word, guessed_correctly = guesses[i] == word)
#----------------------------------------------------------------------------------

#call main. Make sure the code is called when the file is executed
if __name__ == "__main__":
    main()