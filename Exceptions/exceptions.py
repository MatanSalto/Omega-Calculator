class InvalidSymbolException(Exception):
    def __init__(self, index:int, input_string:str) -> None:
        super().__init__(f"\nInvalid character at index {index}\n" + input_string + '\n' + ' '*index + '↑')


class MissingParenthesisException(Exception):
    def __init__(self) -> None:
        super().__init__(f"\nCannot evaluate the expression. Missing parenthesis\n")


class MissingOperandException(Exception):
    def __init__(self, index:int, input_string) -> None:
        super().__init__(f"\nMissing operand at index {index}\n" + input_string + '\n' + ' '*index + '↑')


class MissingOperatorException(Exception):
    def __init__(self, index:int, input_string:str) -> None:
        super().__init__(f"\nMissing operator at index {index}\n" + input_string + '\n' + ' '*index + '↑')


class InvalidOperandException(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)


class EmptyInputString(Exception):
    def __init__(self, message:str= "Empty input string. Nothing to parse") -> None:
        super().__init__(message)


class ParsingInterrupt(Exception):
    def __init__(self, message:str="Parsing has been interruped") -> None:
        super().__init__(message)