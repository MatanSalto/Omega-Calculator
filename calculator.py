from IO.input import ConsoleReader, InputReader
from IO.output import ConsoleOutputPrinter, OutputPrinter
from lexer import Lexer
from parsing import Parser, RecursiveDescentParser
from Exceptions.exceptions import *


class Calculator:

    def __init__(self) -> None:
        self.reader : InputReader = ConsoleReader() # Input device
        self.lexer : Lexer = Lexer() # Lexer object
        self.parser : Parser = RecursiveDescentParser() # Parser object
        self.printer : OutputPrinter = ConsoleOutputPrinter() # Output device

    def activate(self) -> None:
        # Try getting the input string
        try:
            string = self.reader.input("Enter the expression string:\n") + '\0'
        # Catch input excpetions
        except ParsingInterrupt as pi:
            # Print the message
            print(pi)
            # Start the function again
            return self.activate()


        # Try lexing the string
        try:
            tokens = self.lexer.lex(string)
        # Catch invalid symbol exception
        except InvalidSymbolException as ise:
            # Print the message
            print(ise)
            # Start the function again
            return self.activate()
        # Catch empty string exception
        except EmptyInputString as eis:
            # Print the message
            print(eis)
            # Start the function again
            return self.activate()

        
        # Try parsing the expression
        try:
            expression_node = self.parser.parse(tokens, string)
        # Catch syntax exceptions
        except SyntaxException as se:
            # Print the message
            print(se)
            # Start the function again
            return self.activate()

        # Try evaluating the expression
        try:
            result = expression_node.evaluate()
        # Catch invalid operand exception
        except InvalidOperandException as ioe:
            # Print the message
            print(ioe)
            # Call the function again
            return self.activate()

        
        # Try printing the result to the user
        try:
            self.printer.output(f"The result is {result}")
        # Catch output exception
        except ParsingInterrupt as pi:
            # Print the message
            print(pi)
            # Start the function again
            return self.activate()


if __name__ == "__main__":
    # Create a calculator instance and activate it
    calc = Calculator()
    calc.activate()