class InputReader:

    def __init__(self) -> None:
        pass

    def input(self, message:str) -> str:
        pass


class ConsoleReader(InputReader):
    def __init__(self) -> None:
        pass

    def input(self, message:str) -> str:
        return input(message)