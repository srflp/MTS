from colorama import Fore
from colorama import Style


def strip_parentheses(s: str):
    if s[0] == '(' and s[-1] == ')':
        return s[1:-1]
    return s


def color_text(s: str, color: str):
    if color == 'blue':
        return Fore.BLUE + s + Style.RESET_ALL
    elif color == 'green':
        return Fore.GREEN + s + Style.RESET_ALL
    elif color == 'red':
        return Fore.RED + s + Style.RESET_ALL
    return s