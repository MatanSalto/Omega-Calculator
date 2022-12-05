from tokens import *


OPERATORS = ['+', '-', '*', '/', '^', '%', '$', '&', '@', '~', '!', '(', ')', ' ']
# Include space in valid operators even though it is not an operator


class TokenStream:

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


class Lexer:

    def lex_input_string(self, string: str) -> list[Token]:
        # Remove the spaces from the string
        string.replace(' ', '')
        
        # Initialize the list of tokens
        tokens = []
        
        # Initialize the string index
        index = 0

        # Loop through the characters in the string
        while string[index] != '\0':
            # If the character is an operator, append it to the token list as a character
            if string[index] in OPERATORS:
                tokens.append(string[index])
                index += 1
            
            # Else, if the character is a digit, continute reading the digits until reaching a non-digit character
            elif string[index].isdigit():
                number = 0
                digits_after_decimal_point = 0 # counter to indicate how many digits there are after the decimal place

                # Append the digit to the number until the character is not a digit
                while string[index].isdigit():
                    number = number * 10 + int(string[index])
                    index += 1

                # If the character is a decimal point, continue reading the characters after it
                if string[index] == '.':
                    index += 1
            
                    while string[index].isdigit():
                        # Append the digit to the number
                        number = number * 10 + int(string[index])
                        # Increment the counter 
                        digits_after_decimal_point += 1
                        # Increment the index
                        index += 1

                    # At this point, if there are no digits after the decimal place, the number is not valid (it is a number like 2342.)
                    if digits_after_decimal_point == 0:
                        print(f"Expected a digit at index {index}")
                        return

                    # Else, calculate the number and add the corresponding token to the list
                tokens.append(Number(number * (10 ** -digits_after_decimal_point)))

            # Else, the character is not valid
            else:
                print(f"Non valid symbol at index {index}")
                return

        return TokenStream(tokens)
