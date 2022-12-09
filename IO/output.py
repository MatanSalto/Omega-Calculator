class OutputPrinter:
    def __init__(self) -> None:
        pass
    
    def output(self, string:str) -> None:
        pass


class ConsoleOutputPrinter(OutputPrinter):
    def __init__(self) -> None:
        pass

    def output(self, string: str) -> None:
        print(string)