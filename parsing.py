from Algorithms.lexing import Token, TokenStream
from Algorithms.recursive_descent import parse_expression


class Parser:
    """
    This class represents a parser
    """
    def parse(self, token_stream: TokenStream, string:str) -> Token:
        pass


class RecursiveDescentParser(Parser):
    """
    This class represents a recursive descent parser
    """
    
    def parse(self, token_stream: TokenStream, string: str) -> Token:
        return parse_expression(token_stream, string)
