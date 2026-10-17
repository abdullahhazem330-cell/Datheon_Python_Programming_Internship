import csv
import random
words = []
with open('words.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row:
            words.append(row[0])
secret_word = random.choice(words).lower()
display_word = ["_"] * len(secret_word)
attempts = 6
guessed_letters = set()
HANGMAN_PICS = [
    r'''
       +---+
           |
           |
           |
          ===''', r'''
       +---+
       O   |
           |
           |
          ===''', r'''
       +---+
       O   |
       |   |
           |
          ===''', r'''
       +---+
       O   |
      /|   |
           |
          ===''', r'''
       +---+
       O   |
      /|\  |
           |
          ===''', r'''
       +---+
       O   |
      /|\  |
      /    |
          ===''', r'''
       +---+
       O   |
      /|\  |
      / \  |
          ==='''
]
game_over = False
while not game_over:
    print(HANGMAN_PICS[6 - attempts])
    print("\nWord: " + " ".join(display_word))
    print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
    print(f"Attempts left: {attempts}")
    print("-" * 30)
    guess = input("Guess a letter: ").lower()
    if len(guess) != 1 or not guess.isalpha():
        print("\n[!] Please enter a single valid letter.")
        continue
    if guess in guessed_letters:
        print(f"\n[!] You already guessed '{guess}'. Try another letter.")
        continue
    guessed_letters.add(guess)
    if guess in secret_word:
        print(f"\n[+] Good guess! '{guess}' is in the word.")
        for index, letter in enumerate(secret_word):
            if letter == guess:
                display_word[index] = guess
    else:
        attempts -= 1
        print(f"\n[-] Wrong guess! '{guess}' is not in the word.")
    if "_" not in display_word:
        print(HANGMAN_PICS[6 - attempts])
        print("\nWord: " + " ".join(display_word))
        print("\n🎉 Congratulations! You won!")
        game_over = True
    elif attempts == 0:
        print(HANGMAN_PICS[6])
        print(f"\n💀 Game Over! You ran out of attempts. The word was: {secret_word}")
        game_over = True