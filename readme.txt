This is a command line wordle game clone. 
It reads a txt file to create a list of words and then randomly selects one word as the secret word to be guessed, in keeping with the number of letters defined in the code.
The user is allowed up to 6 guesses. At the end of 6 valid guesses, if the user has not guessed correctly, the secret word is displayed.
Letters in each user guess are classified as correct, misplaced and incorrect. 
Using the 'Rich' library, the different categories of letters are color coded to enhance the user experience.
User validation checks that letters in each guess are English letters, that the number of letters is equal to NUM_LETTERS in the code and if a guess has been repeated. Warning messages are shown for each of these scenarios.
If a user hits ctrl+c in the middle of a game, the game ends after showing the secret word.


Summary of key components:
- created a command line application
- read and validated user input
- worked with data in strings, lists and dictionaries
- worked with data in text files
- Used the 'Rich' library to create an attractive user interface