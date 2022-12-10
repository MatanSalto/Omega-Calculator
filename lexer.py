from Algorithms.lexing import lex_input_string
from tokens import Token


class Lexer:
    # This class represents a Lexer object
    
    def lex(self, string:str) -> list[Token]:
        return lex_input_string(string)