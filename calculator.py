from IO.input import ConsoleReader, InputReader
from IO.output import ConsoleOutputPrinter, OutputPrinter
from lexer import Lexer
from parsing import Parser, RecursiveDescentParser


class Calculator:

    def __init__(self) -> None:
        self.reader : InputReader = ConsoleReader() # Input device
        self.lexer : Lexer = Lexer() # Lexer object
        self.parser : Parser = RecursiveDescentParser() # Parser object
        self.printer : OutputPrinter = ConsoleOutputPrinter() # Output device

    def activate(self) -> None:
        # Get the input string
        string = self.reader.input("Enter the expression string:\n") + '\0'

        # Lex the input string
        tokens = self.lexer.lex(string)

        # Parse the sequence of tokens
        expression_node = self.parser.parse(tokens, string)

        # Evaluate the expression
        result = expression_node.evaluate()

        # Output the result to the user
        self.printer.output(f"The result is {result}")



if __name__ == "__main__":
    calc = Calculator()
    calc.activate()