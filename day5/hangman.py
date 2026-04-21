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
    guessing = ["_"] * len(word)
    already_guessed = []

    print(" ".join(guessing))

    while True:
        guess = input("Guess a letter: ").lower()

        if not (guess.isalpha() and len(guess) == 1):
            continue

        if guess in already_guessed:
            print(f"You already guessed [{guess}]")
            continue

        already_guessed.append(guess)

        if guess in word:
            print(f"[{guess}] Was in the word!\n")
            for i, char in enumerate(word):
                if char == guess:
                    guessing[i] = guess
        else:
            print(f"[{guess}] Was NOT in the word!\n")
            lives -= 1

        if "_" not in guessing:
            print(f"You Won!! The word was [{word}]")
            print(f"You finished with {lives} lives left")
            break
        elif lives <= 0:
            print(f"You lost! The word was [{word}]")
            break

        print(" ".join(guessing))
        print(f"You have {lives} lives left\n")

if __name__ == "__main__":
    while True:
        main_game()
        again = input("\nWould you like to play again? y/n: ").lower()
        if again != "y":
            break