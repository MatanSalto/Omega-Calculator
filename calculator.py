from lexer import Lexer
from parsing import Parser

class Calculator:

    def __init__(self) -> None:

        self.lexer = Lexer()
        self.parser = Parser()