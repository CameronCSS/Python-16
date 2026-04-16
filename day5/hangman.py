import requests
import random


def random_word():
    words = [
            "python", "jupiter", "keyboard", "mountain", "ocean", 
            "whisper", "coffee", "palace", "library", "bridge", 
            "sunset", "rhythm", "galaxy", "window", "forest",
            "canvas", "planet", "starlight", "garden", "puzzle"
        ]
    return random.choice(words)

def main_game():
    word = random_word()

    lives = 6
    guessing = []
    already_guess = []

    for _ in word:
        guessing.append("_")

    print(" ".join(guessing))


    while True:
        # ask user for letter
        guess = input("Guess a letter: ").lower()

        # validate guess is a letter
        if guess.isalpha() and len(guess) == 1:
            pass
        else:
            continue

        # Check if they already guessed that
        if guess not in already_guess:
            already_guess.append(guess)
            pass
        else:
            print(f"You already guessed [{guess}]")
            continue

        # check if letter in random word
        if guess in word:
            print(f"[{guess}] Was in the word!\n")
            for i, char in enumerate(word):
                if char == guess:
                    guessing[i] = guess
        else:
            print(f"[{guess}] Was NOT in the word!\n")
            lives -= 1
            pass

        # won
        if "_" not in guessing:
            print(f"You Won!! The word was [{"".join(word)}]")
            print(f"\nYou finished with {lives} lives left")
            break

        # out of lives / Game over
        elif lives <= 0:
            print(f"You lost! The word was [{"".join(word)}]")
            break

        # Print out word with lines and the letters they have guessed
        print(" ".join(guessing))
        print(f"You have {lives} lives left\n")


# Play again
again = input("Would you like to play again? y/n").lower()

if again == "y":
    main_game()


if __name__ == "__main__":
    main_game()