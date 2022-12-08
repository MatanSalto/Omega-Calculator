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

from exceptions import *
from lexer import TokenStream, Lexer
from tokens import *


PRIORITIES = {
    1: [Plus, Minus],
    2: [Mult, Div],
    3: [Power],
    4: [Mod],
    5: [Max, Min, Avg],
}

MAX_PRIORITY = 5


def parse_expression(tokens: TokenStream):
    return parse_binary_expression(tokens, 1)

# Function to parse the initial expression
def parse_binary_expression(tokens: TokenStream, priority):

    if priority > MAX_PRIORITY:
        return parse_factorial_expression(tokens)

    else:
        operators = PRIORITIES[priority]
        a = parse_binary_expression(tokens, priority+1)
        while True:
            if tokens.has_next() and type(tokens.peek()) in operators:
                c = tokens.next()
                b = parse_binary_expression(tokens, priority+1)
                c.left = a
                c.right = b
                a = c  
            else:
                return a


def parse_factorial_expression(tokens: TokenStream):

    a = parse_tilda_expression(tokens)

    while True:
        if tokens.has_next() and type(tokens.peek()) == Factorial:
            c = tokens.next()
            c.operand = a
            a = c
        
        else:
            return a
    

def parse_tilda_expression(tokens: TokenStream):


    if tokens.has_next() and type(tokens.peek()) == Tilda:
        c = tokens.next()
        a = parse_tilda_expression(tokens)
        c.operand = a
        return c

    else:
        return parse_negative_expression(tokens)


def parse_negative_expression(tokens: TokenStream):
    
    if tokens.has_next() and type(tokens.peek()) == Minus:
        c = tokens.next()
        a = parse_negative_expression(tokens)
        return Negative(a.index, '-', a)  

    else:
        return parse_count_digits_expression(tokens)


def parse_count_digits_expression(tokens: TokenStream):
    a = parse_final_expression(tokens)

    while True:
        if tokens.has_next() and type(tokens.peek()) == SumDigits:
            c = tokens.next()
            c.operand = a
            a = c
        
        else:
            return a

def parse_final_expression(tokens: TokenStream):

    # If the next token is a number, pop it and return it
    if tokens.has_next() and type(tokens.peek()) == Number:
        a = tokens.next()
        return a

    elif tokens.has_next() and type(tokens.peek()) == Minus:
        c = tokens.next()
        a = parse_final_expression(tokens)
        return Negative(c.index, '-', a)

    elif tokens.has_next() and type(tokens.peek()) == OpenParen:
        tokens.next()
        a = parse_expression(tokens)
        if tokens.has_next() and type(tokens.peek()) == CloseParen:
            tokens.next()
            return a
        print("Expected )")



class Parser:

    def __init__(self, token_stream: TokenStream) -> None:
        self.token_stream = token_stream

    def parse(self) -> Token:
        return parse_expression(tokens)

if __name__ == "__main__":
    string = "(~~4!) / (2*(2+1))\0"
    lexer = Lexer() 
    tokens = lexer.lex_input_string(string)
    parser = Parser(tokens)

    node = parser.parse()


    print(node.evaluate())

