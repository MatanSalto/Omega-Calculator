from tokens import *
from Exceptions.exceptions import *
from Config.constants import OPERATORS


class TokenStream:
    # This class represents a token stream - an iterator of tokens
    def __init__(self, tokens:list[Token]) -> None:
        self.tokens = tokens
        self.i = 0

    def next(self) -> Token:
        if self.has_next():
            token = self.tokens[self.i]
            self.i += 1
            return token

    def peek(self) -> Token:
        if self.has_next():
            return self.tokens[self.i]

    def has_next(self) -> bool:
        if self.i < len(self.tokens):
            return True

        return False

    def last_token(self) -> Token:
        if self.i == 0:
            return self.tokens[self.i]
        return self.tokens[self.i-1]



def lex_input_string(string) -> TokenStream:
        
    """
    This function performs lexical analysis on the input string, and detects numbers and operators
    Args:
        string (str): _description_

    Returns:
        list[Token]: _description_
    """

    # Initialize the list of tokens
    tokens = []
    
    # Initialize the loop index
    index = 0

    # Loop through the characters in the string
    while string[index] != '\0':
        # Ignore spaces
        if (string[index] == ' '):
            index += 1
            continue

        # If the character is an operator, append it to the token list as a character
        if string[index] in OPERATORS.keys():
            tokens.append(OPERATORS[string[index]](index, string[index]))
            index += 1
        
        # Else, if the character is a digit, continute reading the digits until reaching a non-digit character
        elif string[index].isdigit():
            number = 0
            digits_after_decimal_point = 0 # counter to indicate how many digits there are after the decimal place

            # Append the digit to the number until the character is not a digit
            while string[index].isdigit() or string[index] == ' ':
                # Ignore spaces
                if string[index] == ' ':
                    index += 1
                    continue

                number = number * 10 + int(string[index])
                index += 1

            # If the character is a decimal point, continue reading the characters after it
            if string[index] == '.':
                index += 1
        
                while string[index].isdigit() or string[index] == ' ':
                    if string[index] == ' ':
                        index += 1
                        continue
                    # Append the digit to the number
                    number = number * 10 + int(string[index])
                    # Increment the counter 
                    digits_after_decimal_point += 1
                    # Increment the index
                    index += 1

                # At this point, if there are no digits after the decimal place, the number is not valid (it is a number like 2342.)
                if digits_after_decimal_point == 0:
                    raise InvalidSymbolException(index-1, string)
                # Else, calculate the number and add the corresponding token to the list
            tokens.append(Number(index-1, number * (10 ** -digits_after_decimal_point)))

        # Else, the character is not valid
        else:
            raise InvalidSymbolException(index, string)

    return TokenStream(tokens)