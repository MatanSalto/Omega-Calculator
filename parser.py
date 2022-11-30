"""
  This is the implementation the Recursive Descent parsing algorithm

  The grammar is defined as the following

  E -> ADD
  ADD -> MUL{+|- MUL} // Addition expression can consist other addition expressions
  MUL -> POW{*|\ POW} // Multiplication expression can consist other multiplication expressions
  POW -> MOD{^MOD} // Power expression can consist other power expressions
  MOD -> MAX{$|&|@|MAX}
  MAX -> ~TILDA 
  TILDA -> ~TILDA | FINAL!
  FINAL -> number | (E) | -FINAL
"""

from lexer import TokenStream
from tokens import *


# Function to parse the initial expression
def parseE(tokens: TokenStream):
    return parse_add(tokens)

# Function to parse an addition or subtraction expression
def parse_add(tokens: TokenStream):
    # Parse the left part of the expression using the production 
    a = parse_mul(tokens)

    while True:
        # Ignore spaces
        if tokens.has_next() and isinstance(tokens.peek(), Space):
            tokens.next()
            continue
            
        # If the next token is a plus, parse the rest of the expression
        elif tokens.has_next() and isinstance(tokens.peek(), Plus):
            tokens.next()
            b = parse_mul(tokens)
            a = Plus("+", a, b)
        
        # If the next token is a minus, parse the rest of the expressions
        elif tokens.has_next() and isinstance(tokens.peek(), Minus):
            tokens.next()
            b = parse_mul(tokens)
            a = Minus("-", a, b)

        # Else, there is no production to make, so return the token itself
        else:
            return a


def parse_mul(tokens: TokenStream):
    a = parse_pow(tokens)

    while True:
        # Ignore spaces
        if tokens.has_next() and isinstance(tokens.peek(), Space):
            tokens.next()
            continue
            
        elif tokens.has_next() and isinstance(tokens.peek(), Mult):
            tokens.next()
            b = parse_pow(tokens)
            a = Mult("*", a, b)
        
        elif tokens.has_next() and isinstance(tokens.peek(), Div):
            tokens.next()
            b = parse_pow(tokens)
            a = Div("/", a, b)
        else:
            return a


def parse_pow(tokens: TokenStream):

    a = parse_mod(tokens)
    while True:
        # Ignore spaces
        if tokens.has_next() and isinstance(tokens.peek(), Space):
            tokens.next()
            continue   
        elif tokens.has_next() and isinstance(tokens.peek(), Power):
            tokens.next()
            b = parse_mod(tokens)
            a = Power("%", a, b)
        else:
            return a


def parse_mod(tokens: TokenStream):
    
    a = parse_max(tokens)
    while True:
        # Ignore spaces
        if tokens.has_next() and isinstance(tokens.peek(), Space):
            tokens.next()
            continue   
        elif tokens.has_next() and isinstance(tokens.peek(), Mod):
            tokens.next()
            b = parse_max(tokens)
            a = Mod("^", a, b)
        else:
            return a


def parse_max(tokens: TokenStream):
    a = parse_final(tokens)
    while True:
        # Ignore spaces
        if tokens.has_next() and isinstance(tokens.peek(), Space):
            tokens.next()
            continue   

        elif tokens.has_next() and isinstance(tokens.peek(), Min):
            tokens.next()
            b = parse_final(tokens)
            a = Min("&", a, b)

        elif tokens.has_next() and isinstance(tokens.peek(), Max):
            tokens.next()
            b = parse_final(tokens)
            a = Max("$", a, b)

        elif tokens.has_next() and isinstance(tokens.peek(), Avg):
            tokens.next()
            b = parse_final(tokens)
            a = Avg("@", a, b)

        else:
            return a
    
def parse_final(tokens: TokenStream):

    if tokens.has_next() and isinstance(tokens.peek(), Number):
        a = tokens.next()
        return a

    elif tokens.has_next() and isinstance(tokens.peek(), Minus):
        tokens.next()
        a = parse_final(tokens)
        return Negative('-', a)


def print_tree(node):
    if node != None:
        if isinstance(node, Number):
            print(node.value)
        elif isinstance(node, Negative):
            print(node.value)
            print_tree(node.operand)
        else:
            print_tree(node.left)
            print(node.value)
            print_tree(node.right)

if __name__ == "__main__":

    tokens = TokenStream([Number(10), Avg('@'), Number(4), Mult('*'), Number(3), Minus('-'), Minus('-'), Number(5)])
    
    node = parseE(tokens)
    
    print_tree(node)
    print(node.evaluate())

