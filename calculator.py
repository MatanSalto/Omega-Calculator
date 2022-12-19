from Exceptions.exceptions import *
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

    def activate(self) -> bool:
        """
        This function performs the whole calculation process.
        It gets the input from the user, evaluated the exception and outputs th result
        Returns:
            bool: True if the calculation was successfull, and false otherwise
        """
        # Try getting the input string
        try:
            string = self.reader.input("Enter the expression string:\n") + '\0'
            tokens = self.lexer.lex(string)
            expression_node = self.parser.parse(tokens, string)
            result = expression_node.evaluate()
            self.printer.output(f"The result is {result}")
            return True

        # Catch input excpetions
        except ParsingInterrupt as pi:
            # Print the message
            print(pi)
            # Return False
            return False

        # Catch invalid symbol exception
        except InvalidSymbolException as ise:
            # Print the message
            print(ise)
            # Return False
            return False

        # Catch empty string exception
        except EmptyInputString as eis:
            # Print the message
            print(eis)
            # Return False
            return False

        # Catch syntax exceptions
        except SyntaxException as se:
            # Print the message
            print(se)
            # Return False
            return False

        # Catch invalid operand exception
        except InvalidOperandException as ioe:
            # Print the message
            print(ioe)
            # Return False
            return False

        # Catch overflow error
        except OverflowError as ofe:
            # Print the message
            print(ofe)
            # Return False
            return False
        
        # Catch output exception
        except ParsingInterrupt as pi:
            # Print the message
            print(pi)
            # Return False
            return False


if __name__ == "__main__":
    # Create a calculator instance
    calc = Calculator()
    
    # Activate the calculator over and over again until the calculation is successfull
    while not calc.activate():
        pass