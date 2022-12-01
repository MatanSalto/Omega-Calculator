"""
  This is the implementation the Recursive Descent parsing algorithm

  The grammar is defined as the following:

  E -> ADD 
  ADD -> k{+|- k} // Addition expression can consist other addition expressions
  k -> MUL | -k
  MUL -> POW{*|\ POW} // Multiplication expression can consist other multiplication expressions
  POW -> MOD{^MOD} // Power expression can consist other power expressions
  MOD -> MAX{$|&|@|MAX}
  MAX -> ~TILDA 
  TILDA -> ~TILDA | FINAL!
  FINAL -> number | (E) | -FINAL
"""

from lexer import TokenStream, Lexer
from tokens import *


# Function to parse the initial expression
def parseE(tokens: TokenStream):
    return parse_add(tokens)

# Function to parse an addition or subtraction expression
def parse_add(tokens: TokenStream):
    # Parse the left part of the expression using the production 
    a = parse_k(tokens)

    while True:
        # Ignore spaces
        if tokens.has_next() and tokens.peek() == ' ':
            tokens.next()
            continue
            
        # If the next token is a plus, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '+':
            tokens.next()
            b = parse_k(tokens)
            a = Plus("+", a, b)
        
        # If the next token is a minus, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '-':
            tokens.next()
            b = parse_k(tokens)
            a = Minus("-", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_k(tokens: TokenStream):

    while tokens.has_next() and tokens.peek() == ' ':
        tokens.next()

    if tokens.has_next() and tokens.peek() == '-':
        tokens.next()
        return Negative('-', parse_mul(tokens))

    return parse_mul(tokens)

def parse_mul(tokens: TokenStream):
    a = parse_pow(tokens)

    while True:
        # Ignore spaces
        if tokens.has_next() and tokens.peek() == ' ':
            tokens.next()
            continue
        
        # If the next token is a multplication, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '*':
            tokens.next()
            b = parse_pow(tokens)
            a = Mult("*", a, b)
        
        # If the next token is a division, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '/':
            tokens.next()
            b = parse_pow(tokens)
            a = Div("/", a, b)

        # Else, there is not production to make, so return the token itself
        else:
            return a


def parse_pow(tokens: TokenStream):

    a = parse_mod(tokens)
    while True:
        # Ignore spaces
        if tokens.has_next() and tokens.peek() == ' ':
            tokens.next()
            continue   

        # If the next token is a power, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '^':
            tokens.next()
            b = parse_mod(tokens)
            a = Power("^", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_mod(tokens: TokenStream):
    
    a = parse_max(tokens)
    while True:
        # Ignore spaces
        if tokens.has_next() and tokens.peek() == ' ':
            tokens.next()
            continue   

        # If the next token is a mod, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '%':
            tokens.next()
            b = parse_max(tokens)
            a = Mod("%", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_max(tokens: TokenStream):
    a = parse_factorial(tokens)
    while True:
        # Ignore spaces
        if tokens.has_next() and tokens.peek() == ' ':
            tokens.next()
            continue   

        # If the next token is a min, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '&':
            tokens.next()
            b = parse_factorial(tokens)
            a = Min("&", a, b)

        # If the next token is a max, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() ==  '$':
            tokens.next()
            b = parse_factorial(tokens)
            a = Max("$", a, b)

        # If the next token is an avg, parse the rest of the expression
        elif tokens.has_next() and tokens.peek() == '@':
            tokens.next()
            b = parse_factorial(tokens)
            a = Avg("@", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_factorial(tokens: TokenStream):

    a = parse_tilda(tokens)

    while True:

        if tokens.has_next() and tokens.peek() == ' ':
            tokens.next()
            continue

        elif tokens.has_next() and tokens.peek() == '!':
            tokens.next()
            a = Factorial('!',a)
        
        else:
            return a
    

def parse_tilda(tokens: TokenStream):

    while tokens.has_next() and tokens.peek() == ' ':
        tokens.next()

    if tokens.has_next() and tokens.peek() == '~':
        tokens.next()
        a = parse_tilda(tokens)
        return Tilda('~', a)

    else:
        return parse_final(tokens)


def parse_final(tokens: TokenStream):

    # Ignore spaces
    while tokens.has_next() and tokens.peek() == ' ':
        tokens.next()

    # If the next token is a number, pop it and return it
    if tokens.has_next() and isinstance(tokens.peek(), Number):
        a = tokens.next()
        return a

    elif tokens.has_next() and tokens.peek() == '-':
        tokens.next()
        a = parse_final(tokens)
        return Negative('-', a)

    elif tokens.has_next() and tokens.peek() == '(':
        tokens.next()
        a = parseE(tokens)
        if tokens.has_next() and tokens.peek() == ')':
            tokens.next()
            return a
        print("Expected )")




class Parser:

    def __init__(self, token_stream: TokenStream) -> None:
        self.token_stream = token_stream

    def parse(self) -> Token:
        return parseE(tokens)

if __name__ == "__main__":

    string = "-5&2\0"
    lexer = Lexer() 
    tokens = lexer.lex_input_string(string)
    parser = Parser(tokens)

    node = parser.parse()


    print(node.evaluate())

