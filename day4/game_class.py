from random import randint

class Game:
    # Initialize the class
    # Hardcode variables that dont change
    # set to nothing for those we need to get
    def __init__(self):
        self.name = ""
        self.number = None
        self.guesses = 10
        self.guess_range = (1, 100)
        self.already_guessed = set()
        
    def set_name(self):
        self.name = input("What is your name? ")
        
    def set_rand_num(self):
        self.number = randint(*self.guess_range)
    
    def greet(self):
        self.empty_spacer()
        
        # greet the user
        print(f"Welcome {self.name}")
        self.filled_spacer()
        print(f"This is a number guessing game!")
        self.empty_spacer()
        
        # Tell user they have to guess a number between x>y 
        print(f"You have to guess a number between {self.guess_range[0]} and {self.guess_range[1]}")
        
        # Tell them how many guesses they get
        print(f"You only get {self.guesses} guesses.")
        self.empty_spacer()
        
        print("------Good luck!!------")
        self.empty_spacer()
        
    def print_guesses(self):
        print(f"\nYou have {self.guesses} guesses left.\n")    
    
    def empty_spacer(self):
        print()
        
    def filled_spacer(self):
        print(f"\n--------------------------------\n")
    
    def replay(self):
        again = input("Play again? (y/n): ")
        if again.lower() == "y":
             # reset game state
            self.__init__()
            self.run()    
            
    def thank(self):
        self.empty_spacer()
        self.filled_spacer()
        print("Thank you for playing!!")
        self.filled_spacer()
        self.empty_spacer()
        
    def play(self):
        while True:
            user_guess = input("Guess a number: ")
            
            # check user entered a number
            try:
                user_guess = int(user_guess)
            # if it wasnt a number, prompt them
            except ValueError:
                print("\nPlease guess an actual number")
                self.empty_spacer()
                self.filled_spacer()
                continue
            
            # If user guessed the number WINNER
            if user_guess == self.number:
                self.empty_spacer()
                self.filled_spacer()
                print(f"YOU WIN!! The number was {self.number}")
                break
            
            # if guesses are out GAME OVER
            elif self.guesses <= 1:
                self.empty_spacer()
                self.filled_spacer()
                print("You ran out of guesses")
                print("----- GAME OVER -----")
                print(f"The number was [{self.number}]")
                break
            
            # if number out of range, warn them its out of range
            elif user_guess not in range(*self.guess_range):
                self.empty_spacer()
                self.filled_spacer()
                print(f"You have to guess a number between {self.guess_range[0]} and {self.guess_range[1]}")
            
            # If they already guessed that number
            elif user_guess in self.already_guessed:
                self.empty_spacer()
                self.filled_spacer()
                print(f"You already guessed [{user_guess}]")
                self.empty_spacer()
                
            # if number was less, take a guess away. and say guess was low
            elif user_guess < self.number:
                self.empty_spacer()
                self.filled_spacer()
                print(f"[{user_guess}] is too low. Try again.")
                self.guesses -= 1
                self.print_guesses()
                self.already_guessed.add(user_guess)
                
            # if number was more, take a guess away. and say guess was high
            elif user_guess > self.number:
                self.empty_spacer()
                self.filled_spacer()
                print(f"[{user_guess}] is too High. Try again.")
                self.print_guesses()
                self.guesses -= 1
                self.already_guessed.add(user_guess)
                
            # Error catch if all else fails
            else:
                self.empty_spacer()
                self.filled_spacer()
                print("Error. Try again...")
                break
        
        # Ask if they want to play again
        self.replay()
            
    # Run program
    def run(self):
        self.set_name()
        self.greet()
        self.set_rand_num()
        self.play()