from Config.constants import OPERATORS
from Exceptions.exceptions import *
from tokens import *


class TokenStream:
    # This class represents a token stream - an iterator of tokens
    def __init__(self, tokens:list[Token]) -> None:
        self.tokens = tokens
        self.i = 0

    def next(self) -> Token:
        """
        this method pop the next token in the stream and returns it

        Returns:
            Token: the next token in the stream
        """
        if self.has_next():
            token = self.tokens[self.i]
            self.i += 1
            return token

    def peek(self) -> Token:
        """
        this method returns the next token in the stream without popping it

        Returns:
            Token: the next token in the stream
        """
        if self.has_next():
            return self.tokens[self.i]

    def look_ahead(self) -> Token:
        """
        this token returns the token after the next one in the stream without popping it

        Returns:
            Token: the token after the next one in the stream
        """
        if self.has_double_next():
            return self.tokens[self.i+1]

    def has_next(self) -> bool:
        """
        this method checks if the stream has a next token

        Returns:
            bool: True if the stream has a next token, and False otherwise
        """
        if self.i < len(self.tokens):
            return True

        return False

    def has_double_next(self) -> bool:
        """
        this method checks if the stream has at least two next tokens

        Returns:
            bool: True if the stream has at least two next tokens, and False otherwise
        """
        return self.i < len(self.tokens)-1

    def last_token(self) -> Token:
        """
        this method returns the last token that was popped out of the stream

        Returns:
            Token: the last token that was popped out of the stream
        """
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

    # If the string is empty or only whitespaces, raise an exception
    if string == '\0' or all([char.isspace() for char in string[:-1]]) :
        raise EmptyInputString()

    # Loop through the characters in the string
    while string[index] != '\0':
        # Ignore whitespaces
        if string[index].isspace():
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
            while string[index].isdigit() or string[index].isspace():
                # Ignore whitespaces
                if string[index].isspace():
                    index += 1
                    continue

                # Add the digit to the number
                number = number * 10 + int(string[index])
                index += 1

            # If the character is a decimal point, continue reading the characters after it
            if string[index] == '.':
                index += 1
        
                while string[index].isdigit() or string[index].isspace():
                    # Ignore whitespaces
                    if string[index].isspace():
                        index += 1
                        continue

                    # Append the digit to the number
                    number = number * 10 + int(string[index])
                    # Increment the counter 
                    digits_after_decimal_point += 1
                    # Increment the index
                    index += 1

                # At this point, if there are no digits after the decimal place, the number is not valid (like the number 2342.)
                if digits_after_decimal_point == 0:
                    raise InvalidSymbolException(index-1, string)
                # Else, calculate the total number and add the corresponding token to the list
            tokens.append(Number(index-1, number * (10 ** -digits_after_decimal_point)))

        # Else, the character is not valid, so raise an exception
        else:
            raise InvalidSymbolException(index, string)

    # Return a TokenStream object of the tokens list
    return TokenStream(tokens)