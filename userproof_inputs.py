"""Module to take user input according to certain criteria"""

from colorama import Fore, Style


def ask_user_for_number(message: str) -> int:
    """Keeps requesting an input from the user with the given msg until an integer is entered"""
    user_input = ""
    while True:
        user_input = input(Fore.BLUE + message + Style.RESET_ALL)
        if user_input.isnumeric():
            num = int(user_input)
            return num
        print("Invalid input - please try again.\n")


def ask_user_for_specific_inputs(message: str, valid_inputs: list[str]) -> str:
    """Keeps asking user for input until it is in the valid_inputs list"""
    user_input = ""
    while True:
        user_input = input(Fore.BLUE + message + Style.RESET_ALL)
        if user_input in valid_inputs:
            return user_input
        print("Invalid input - please try again.\n")
