from Exceptions.exceptions import ParsingInterrupt

class OutputPrinter:
    def __init__(self) -> None:
        pass
    
    def output(self, string:str) -> None:
        pass


class ConsoleOutputPrinter(OutputPrinter):
    def __init__(self) -> None:
        pass

    def output(self, string: str) -> None:
        try:
            print(string)
        # Catch IO errors
        except IOError as ioe:
            print(ioe.__cause__)
            # Raise paring interrupt exception
            raise ParsingInterrupt()

        # Catch the rest of the exceptions:
        except RuntimeError as rte:
            print(rte.__cause__)
            # Raise paring interrupt exception
            raise ParsingInterrupt()