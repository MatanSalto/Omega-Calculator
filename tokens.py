# Define the Token class
class Token:
    def __init__(self, type:str, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"<{self.type}, {self.value}>"

    def evaluate(self) -> float:
        pass

class Number(Token):
    def __init__(self, value:float) -> None:
        super().__init__("Number", value)

    def evaluate(self) -> float:
        return self.value


class Operator(Token):
    def __init__(self, value) -> None:
        super().__init__("Operator", value)


class UnaryOperator(Operator):
    def __init__(self, value:str, operand:Token = None) -> None:
        super().__init__(value)
        self.operand = operand


class BinaryOperator(Operator):
    def __init__(self, value:str, left:Token = None, right:Token = None) -> None:
        super().__init__(value)
        self.left = left
        self.right = right

        
class Factorial(UnaryOperator):
    def __init__(self, value: str, operand: Token = None) -> None:
        super().__init__(value, operand)

    def evaluate(self) -> float:
        return self._factorial(self.operand.evaluate())

    def _factorial(self, n:int) -> int:
        if n == 0: return 1
        return n * self._factorial(n-1)


class Tilda(UnaryOperator):
    def __init__(self, value: str, operand: Token = None) -> None:
        super().__init__(value, operand)

    def evaluate(self) -> float:
        return -1 * self.operand.evaluate()


class Negative(UnaryOperator):
    def __init__(self, value: str, operand: Token = None) -> None:
        super().__init__(value, operand)

    def evaluate(self) -> float:
        return -1 * self.operand.evaluate()


class SumDigits(UnaryOperator):
    def __init__(self, value: str, operand: Token = None) -> None:
        super().__init__(value, operand)

    def evaluate(self) -> float:
        return self._count_digits(self.operand.evaluate())

    def _count_digits(self, num):
        sum = 0
        for digit in str(num):
            sum += int(digit)

        return sum

class Plus(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() + self.right.evaluate()


class Minus(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() - self.right.evaluate()


class Mult(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() * self.right.evaluate()


class Div(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() / self.right.evaluate()


class Power(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() ** self.right.evaluate()


class Mod(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() % self.right.evaluate()


class Max(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:
        
        a = self.left.evaluate()
        b = self.right.evaluate()

        return a if a > b else b


class Min(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:
        
        a = self.left.evaluate()
        b = self.right.evaluate()

        return a if a < b else b


class Avg(BinaryOperator):
    def __init__(self, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(value, left, right)

    def evaluate(self) -> float:        
        return (self.left.evaluate() + self.right.evaluate()) / 2



