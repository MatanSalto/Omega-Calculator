from Exceptions.exceptions import EmptyInputString, ParsingInterrupt


class InputReader:

    def __init__(self) -> None:
        pass

    def input(self, message:str) -> str:
        pass


class ConsoleReader(InputReader):
    def __init__(self) -> None:
        pass

    def input(self, message:str) -> str:
        # Try to input the string from the user
        try:
            string = input(message)
            
        # Catch keyboard interrupt
        except KeyboardInterrupt as kbi:
            print(kbi.__cause__)
            # Raise parsing interrupt exception
            raise ParsingInterrupt()
        
        # Catch end of file error
        except EOFError as eofe:
            print(eofe.__cause__)
            # Raise parsing interrupt exception
            raise ParsingInterrupt()

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

        # Return the string
        return string