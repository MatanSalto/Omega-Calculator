"""
  This is the implementation the Recursive Descent parsing algorithm

  The grammar is defined as the following:

  E -> ADD 
  ADD -> MUL{+|- MUL}
  MUL -> POW{*|\ POW}
  POW -> MOD{^MOD}
  MOD -> MAX{$|&|@|MAX}
  MAX -> FACT
  FACT -> FACT! | TILDA
  TILDA -> ~TILDA | NEG
  NEG -> -NEG | COUNT
  COUNT -> COUNT# | FINAL
  FINAL -> -FINAL | number | (E) |
"""

from lexer import TokenStream, Lexer
from tokens import *


# Function to parse the initial expression
def parse_expression(tokens: TokenStream):
    return parse_addition_subtraction_expression(tokens)

# Function to parse an addition or subtraction expression
def parse_addition_subtraction_expression(tokens: TokenStream):
    # Parse the left part of the expression using the production 
    a = parse_multiplication_division_expression(tokens)

    while True:
            
        # If the next token is a plus, parse the rest of the expression
        if tokens.has_next() and tokens.peek() == '+':
            tokens.next()
            b = parse_multiplication_division_expression(tokens)
            a = Plus("+", a, b)
        
        # If the next token is a minus, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '-':
            tokens.next()
            b = parse_multiplication_division_expression(tokens)
            a = Minus("-", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_multiplication_division_expression(tokens: TokenStream):
    a = parse_power_expression(tokens)

    while True:
     
        # If the next token is a multplication, parse the rest of the expression
        if tokens.has_next() and tokens.peek() == '*':
            tokens.next()
            b = parse_power_expression(tokens)
            a = Mult("*", a, b)
        
        # If the next token is a division, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '/':
            tokens.next()
            b = parse_power_expression(tokens)
            a = Div("/", a, b)

        # Else, there is not production to make, so return the token itself
        else:
            return a


def parse_power_expression(tokens: TokenStream):

    a = parse_mod_expression(tokens)
    while True:

        # If the next token is a power, parse the rest of the expression
        if tokens.has_next() and tokens.peek() == '^':
            tokens.next()
            b = parse_mod_expression(tokens)
            a = Power("^", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_mod_expression(tokens: TokenStream):
    
    a = parse_max_min_avg_expression(tokens)
    while True:

        # If the next token is a mod, parse the rest of the expression
        if tokens.has_next() and tokens.peek() == '%':
            tokens.next()
            b = parse_max_min_avg_expression(tokens)
            a = Mod("%", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_max_min_avg_expression(tokens: TokenStream):
    a = parse_factorial_expression(tokens)
    while True:  

        # If the next token is a min, parse the rest of the expression
        if tokens.has_next() and tokens.peek() == '&':
            tokens.next()
            b = parse_factorial_expression(tokens)
            a = Min("&", a, b)

        # If the next token is a max, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() ==  '$':
            tokens.next()
            b = parse_factorial_expression(tokens)
            a = Max("$", a, b)

        # If the next token is an avg, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '@':
            tokens.next()
            b = parse_factorial_expression(tokens)
            a = Avg("@", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_factorial_expression(tokens: TokenStream):

    a = parse_tilda_expression(tokens)

    while True:
        if tokens.has_next() and tokens.peek() == '!':
            tokens.next()
            a = Factorial('!',a)
        
        else:
            return a
    

def parse_tilda_expression(tokens: TokenStream):

    if tokens.has_next() and tokens.peek() == '~':
        tokens.next()
        a = parse_negative_expression(tokens)
        return Tilda('~', a)

    else:
        return parse_negative_expression(tokens)


def parse_negative_expression(tokens: TokenStream):
    
    if tokens.has_next() and tokens.peek() == '-':
        tokens.next()
        a = parse_count_digits_expression(tokens)
        return Negative('-', a)

    else:
        return parse_count_digits_expression(tokens)

def parse_count_digits_expression(tokens: TokenStream):
    a = parse_final_expression(tokens)

    while True:
        if tokens.has_next() and tokens.peek() == '#':
            tokens.next()
            a = SumDigits('#',a)
        
        else:
            return a

def parse_final_expression(tokens: TokenStream):

    # If the next token is a number, pop it and return it
    if tokens.has_next() and isinstance(tokens.peek(), Number):
        a = tokens.next()
        return a

    elif tokens.has_next() and tokens.peek() == '-':
        tokens.next()
        a = parse_final_expression(tokens)
        return Negative('-', a)

    elif tokens.has_next() and tokens.peek() == '(':
        tokens.next()
        a = parse_expression(tokens)
        if tokens.has_next() and tokens.peek() == ')':
            tokens.next()
            return a
        print("Expected )")




class Parser:

    def __init__(self, token_stream: TokenStream) -> None:
        self.token_stream = token_stream

    def parse(self) -> Token:
        return parse_expression(tokens)

if __name__ == "__main__":

    string = "(2+1)!!\0"
    lexer = Lexer() 
    tokens = lexer.lex_input_string(string)
    parser = Parser(tokens)

    node = parser.parse()


    print(node.evaluate())

