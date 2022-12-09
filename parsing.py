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

# Function to parse the initial expression
def parse_expression(tokens: TokenStream):
    return parse_binary_expression(tokens, 1)

# Function to parse binary expressions
def parse_binary_expression(tokens: TokenStream, priority:int) -> Token:
    """
    This recursive function parses a binary expression
    Args:
        tokens (TokenStream): the sequence of tokens to parse
        priority (int): the current priority of the operators

    Returns:
        Token: a token node representing the expression
    """
    
    # Base case: if we reached the max priority, try parsing the rest of the expression as a factorial expression
    if priority > MAX_PRIORITY:
        return parse_factorial_expression(tokens)

    else:
        # Get the valid operators for the current priority
        operators = PRIORITIES[priority]
        # Parse the left hand side of the expression
        a = parse_binary_expression(tokens, priority+1)

        while True:
            # If the next token is a valid operator
            if tokens.has_next() and type(tokens.peek()) in operators:
                # Get the operator's node
                c = tokens.next()
                # Parse the right hand side of the expression
                b = parse_binary_expression(tokens, priority+1)
                # Set the left hand and right hand sides of the expression as the operator's children
                c.left = a
                c.right = b
                # Set a to be the operator node
                a = c  
            # Else, there is no more valid operators at the current priority, so return the node itself
            else:
                return a


def parse_factorial_expression(tokens: TokenStream) -> Token:
    """
    This function parses a factorial expression
    Args:
        tokens (TokenStream): the sequence of tokens

    Returns:
        Token: a token node representing the expression
    """

    # Parse the left side of the expression
    a = parse_tilda_expression(tokens)

    while True:
        # If the next token is a factorial
        if tokens.has_next() and type(tokens.peek()) == Factorial:
            # Get the factorial operator node
            c = tokens.next()
            # Set the left side as the factorial node child
            c.operand = a
            # Set a to be the factorial node 
            a = c
        
        # Else, there is no more factorial operators in the expression, so return the node itself
        else:
            return a
    

def parse_tilda_expression(tokens: TokenStream) -> Token:
    """
    This function parses a tilda expression
    Args:
        tokens (TokenStream): the sequence of tokens

    Returns:
        Token: a token node representing the expression
    """
    
    # If the next token is a tilda operator
    if tokens.has_next() and type(tokens.peek()) == Tilda:
        # Get the tilda operator node
        c = tokens.next()
        # Parse the right side of the expression
        a = parse_tilda_expression(tokens)
        # Set the right side as the tilda node child
        c.operand = a
        # Return the tilda node
        return c
    
    # Else, there is no tilda operator in the expression, so try to parse the rest of the expression
    else:
        return parse_sum_digits_expression(tokens)


def parse_sum_digits_expression(tokens: TokenStream) -> Token:
    """
    This function parses a sum-digits expression
    Args:
        tokens (TokenStream): the sequence of tokens

    Returns:
        Token: a token node representing the expression
    """

    # Parse the left side of the expression
    a = parse_final_expression(tokens)

    while True:
        # If the next token is a sum-digits operator
        if tokens.has_next() and type(tokens.peek()) == SumDigits:
            # Get the SumDigits operator node
            c = tokens.next()
            # Set the left side as the operator's child
            c.operand = a
            # Set a to be the operator node
            a = c
        
        # Else, there is no more SumDigits operators in the expression, so return the node itself
        else:
            return a

def parse_final_expression(tokens: TokenStream) -> Token:
    """
    This function parses a final expression
    Args:
        tokens (TokenStream): the sequence of tokens

    Returns:
        Token: a token node representing the expression
    """

    # If the next token is a number, pop it and return it
    if tokens.has_next() and type(tokens.peek()) == Number:
        a = tokens.next()
        return a

    # If the next token is a minus operator
    elif tokens.has_next() and type(tokens.peek()) == Minus:
        # Get the minus operator node
        c = tokens.next()
        # Parse the left side of the expression
        a = parse_final_expression(tokens)
        # Return a negative node with the left side as its child
        return Negative(c.index, '-', a)
    
    # Else, if the next token is an '('
    elif tokens.has_next() and type(tokens.peek()) == OpenParen:
        tokens.next()
        # Parse the inner expression
        a = parse_expression(tokens)
        # If the next token is a ')', pop the token and return the expression
        if tokens.has_next() and type(tokens.peek()) == CloseParen:
            tokens.next()
            return a
        
        # Else, raise an exception
        raise MissingParenthesisException()



class Parser:

    def __init__(self, token_stream: TokenStream) -> None:
        self.token_stream = token_stream

    def parse(self) -> Token:
        return parse_expression(tokens)

if __name__ == "__main__":
    string = "2^(~--2&10)\0"
    lexer = Lexer() 
    tokens = lexer.lex_input_string(string)
    parser = Parser(tokens)

    node = parser.parse()

    print(node.evaluate())
