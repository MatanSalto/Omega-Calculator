from Exceptions.exceptions import *
from Algorithms.lexing import TokenStream
from tokens import *
from Config.constants import PRIORITIES


MAX_PRIORITY = 5  # The maximum priority for a binary operator


# Function to parse the initial expression
def parse_expression(tokens: TokenStream, string:str, in_paren=False) -> Token:
    """
    This function parses the expression
    Args:
        tokens (TokenStream): the sequence of tokens
        string (str): the original input string (to report errors)
        in_paren (bool, optional): is the current expression is in parenthasis. Defaults to False.

    Returns:
        Token: a token node representing the expression
    """
    return parse_binary_expression(tokens, 1, string, in_paren)

# Function to parse binary expressions
def parse_binary_expression(tokens: TokenStream, priority:int, string:str, in_paren=False) -> Token:
    """
    This recursive function parses a binary expression
    Args:
        tokens (TokenStream): the sequence of tokens to parse
        priority (int): the current priority of the operators
        string (str): the original input sting (to report errors)
        in_paren (bool, optional): is the current expression is in parenthasis. Defaults to False.

    Returns:
        Token: a token node representing the expression
    """
    
    # Base case: if we reached the max priority, try parsing the rest of the expression as a factorial expression
    if priority > MAX_PRIORITY:
        return parse_factorial_expression(tokens, string, in_paren)

    else:
        # Get the valid operators for the current priority
        operators = PRIORITIES[priority]

        # Parse the left hand side of the expression
        a = parse_binary_expression(tokens, priority+1, string, in_paren)

        # If a is null, raise an exception
        if not a:
            raise MissingOperandException(tokens.last_token().index, string)

        while True:
            # If the next token is a valid operator
            if tokens.has_next() and type(tokens.peek()) in operators:
                # Get the operator's node
                c = tokens.next()

                # Parse the right hand side of the expression
                b = parse_binary_expression(tokens, priority+1, string, in_paren)

                # If the right hand side, is null, raise an exception
                if not b:
                    raise MissingOperandException(c.index, string)

                # Set the left hand and right hand sides of the expression as the operator's children
                c.left = a
                c.right = b

                # Set a to be the operator node
                a = c  

            # Else, there is no more valid operators at the current priority
            else:
                # If the next token is a number, a '(' or a '~', raise an exception
                if type(tokens.peek()) == Number or type(tokens.peek()) == OpenParen or type(tokens.peek()) == Tilda:
                    raise MissingOperatorException(tokens.peek().index, string)

                # If the expression is not in parenthesis and we encountered a ')', raise an exception
                if not in_paren and type(tokens.peek()) == CloseParen:
                    raise MissingParenthesisException()
                
                # Else, return the node itself
                return a


def parse_factorial_expression(tokens: TokenStream, string:str, in_paren=False) -> Token:
    """
    This function parses a factorial expression
    Args:
        tokens (TokenStream): the sequence of tokens
        string (str): the original input sting (to report errors)
        in_paren (bool, optional): is the current expression is in parenthasis. Defaults to False.

    Returns:
        Token: a token node representing the expression
    """

    # Parse the left side of the expression
    a = parse_tilda_expression(tokens, string, in_paren)

    if not a:
        raise MissingOperandException(tokens.last_token().index, string)

    while True:
        # If the next token is a factorial
        if tokens.has_next() and type(tokens.peek()) == Factorial:
            # Get the factorial operator node
            c = tokens.next()
            # Set the left side as the factorial node child
            c.operand = a
            # Set a to be the factorial node 
            a = c
        
        # Else, there is no more factorial operators in the expression
        else:
            # If the expression is not in parenthesis and we encountered a ')', raise an exception
            if not in_paren and type(tokens.peek()) == CloseParen:
                    raise MissingParenthesisException()

            # Else, return the node itself
            return a
    

def parse_tilda_expression(tokens: TokenStream, string:str, in_paren=False) -> Token:
    """
    This function parses a tilda expression
    Args:
        tokens (TokenStream): the sequence of tokens
        string (str): the original input sting (to report errors)
        in_paren (bool, optional): is the current expression is in parenthasis. Defaults to False.

    Returns:
        Token: a token node representing the expression
    """
    
    # If the next token is a tilda operator
    if tokens.has_next() and type(tokens.peek()) == Tilda:
        # Get the tilda operator node
        c = tokens.next()
        # Parse the right side of the expression
        a = parse_tilda_expression(tokens, string, in_paren)

        if not a:
            raise MissingOperandException(c.index, string)
        # Set the right side as the tilda node child
        c.operand = a
        # Return the tilda node
        return c
    
    # Else, there is no tilda operator in the expression
    else:
        # If the expression is not in parenthesis and we encountered a ')', raise an exception
        if not in_paren and type(tokens.peek()) == CloseParen:
            raise MissingParenthesisException()

        # Else try parsing the rest of the expression
        return parse_negative_expression(tokens, string, in_paren)



def parse_negative_expression(tokens: TokenStream, string:str, in_paren=False):
    """
    This function parses a negative expression
    Args:
        tokens (TokenStream): the sequence of tokens
        string (str): the original input sting (to report errors)
        in_paren (bool, optional): is the current expression is in parenthasis. Defaults to False.

    Returns:
        Token: a token node representing the expression
    """
    # If the next token in a minus
    if tokens.has_next() and type(tokens.peek()) == Minus:
        # Pop the next token
        c = tokens.next()
        # Parse the rest of the expression
        a = parse_tilda_expression(tokens, string, in_paren)

        if not a:
            raise MissingOperandException(c.index, string)
        
        # Return the negative node  
        return Negative(c.index, '-', a)

    else:
        # If the expression is not in parenthesis and we encountered a ')', raise an exception
        if not in_paren and type(tokens.peek()) == CloseParen:
            raise MissingParenthesisException()

        # Else, try parsing the rest of the expression
        return parse_sum_digits_expression(tokens, string, in_paren)


def parse_sum_digits_expression(tokens: TokenStream, string:str, in_paren=False) -> Token:
    """
    This function parses a sum-digits expression
    Args:
        tokens (TokenStream): the sequence of tokens
        string (str): the original input sting (to report errors)
        in_paren (bool, optional): is the current expression is in parenthasis. Defaults to False.

    Returns:
        Token: a token node representing the expression
    """

    # Parse the left side of the expression
    a = parse_final_expression(tokens, string)

    if not a:
        raise MissingOperandException(tokens.last_token().index, string)

    while True:
        # If the next token is a sum-digits operator
        if tokens.has_next() and type(tokens.peek()) == SumDigits:
            # Get the SumDigits operator node
            c = tokens.next()
            # Set the left side as the operator's child
            c.operand = a
            # Set a to be the operator node
            a = c
        
        # Else, there is no more SumDigits operators in the expression
        else:
            # If the expression is not in parenthesis and we encountered a ')', raise an exception
            if not in_paren and type(tokens.peek()) == CloseParen:
                raise MissingParenthesisException()

            # Else, return the node itself
            return a

def parse_final_expression(tokens: TokenStream, string:str) -> Token:
    """
    This function parses a final expression
    Args:
        tokens (TokenStream): the sequence of tokens
        string (str): the original input sting (to report errors)
        in_paren (bool, optional): is the current expression is in parenthasis. Defaults to False.

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
        a = parse_final_expression(tokens, string)
        # Return a negative node with the left side as its child
        return Negative(c.index, '-', a)
    
    # Else, if the next token is an '('
    elif tokens.has_next() and type(tokens.peek()) == OpenParen:
        # If the previous token is a tilda, raise an exception
        if type(tokens.last_token()) == Tilda:
            raise InvalidOperandException("Invalid operand for the tilda operator. Only numbers are allowed")
        
        # Pop the '('
        tokens.next()

        # Parse the inner expression
        a = parse_expression(tokens, string, True)

        # If the next token is a ')', pop the token and return the expression
        if tokens.has_next() and type(tokens.peek()) == CloseParen:
            tokens.next()
            return a
        
        # Else, raise an exception
        raise MissingParenthesisException()
