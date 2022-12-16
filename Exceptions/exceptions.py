# Lexical exceptions

# This exception is raised when the lexer encounters an invalid symbol
class InvalidSymbolException(Exception):
    def __init__(self, index:int, input_string:str) -> None:
        super().__init__(f"\nInvalid character at index {index}\n" + input_string + '\n' + ' '*index + '↑')


# This exception is raised when the lexer encounters an empty string an input
class EmptyInputString(Exception):
    def __init__(self, message:str= "Empty input string. Nothing to parse") -> None:
        super().__init__(message)



# Syntax exceptions

# This exception is raised when the parser encounters an invalid expression structure (abstract class)
class SyntaxException(Exception):
    def __init__(self, message: int) -> None:
        super().__init__(message)

# This exception is raised when the parser encounters a missing parenthesis in an expression
class MissingParenthesisException(SyntaxException):
    def __init__(self) -> None:
        super().__init__(f"\nCannot evaluate the expression. Missing parenthesis\n")

# This exception is raised when the parser encounters a missing operand in an expression
class MissingOperandException(SyntaxException):
    def __init__(self, index:int, input_string) -> None:
        super().__init__(f"\nMissing operand at index {index}\n" + input_string + '\n' + ' '*index + '↑')

# This exception is raised when the parser encounters a missing operator in an expression
class MissingOperatorException(SyntaxException):
    def __init__(self, index:int, input_string:str) -> None:
        super().__init__(f"\nMissing operator at index {index}\n" + input_string + '\n' + ' '*index + '↑')

# This exception is raised when an invalid operand is encountered during the evaluation of the expression (e.g factorial of a negative number)
class InvalidOperandException(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)



# Other excpetions

# This exception is raised when there is some keyboard interrupt during the parsing of the expression
class ParsingInterrupt(Exception):
    def __init__(self, message:str="Parsing has been interruped") -> None:
        super().__init__(message)