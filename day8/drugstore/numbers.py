"""
This program is a ticketing system that assigns a ticket number to customer 
Generators and Decorators for the main ticketing program will go here
"""

def give_number(function):
    """
    This is the decorated function that runs the passes the internal function
    """

    def printout():
        """
        This is the printout function that prints results from each generator object
        """

        print(f'Your number is: {next(function)}')
        print('Please Wait... someone will be with you shortly. \n')

    return printout

def ticket_generator(prefix):
    """
    This is the main generator.
    Instead of creating 3 separate generators we pass the prefix and use a single generator.
    Declaring in main function gives each decleration its own generator object.
    """

    num = 1
    while True:
        yield f"{prefix}-{num}"
        num += 1
