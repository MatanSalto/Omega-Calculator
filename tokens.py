from exceptions import *

# Define the Token class
class Token:
    def __init__(self, index:int, type:str, value) -> None:
        self.index = index
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"<{self.index}, {self.type}, {self.value}>"

    def evaluate(self) -> float:
        pass

class Number(Token):
    def __init__(self, index:int, value:float) -> None:
        super().__init__(index, "Number", value)

    def evaluate(self) -> float:
        return self.value


class Operator(Token):
    def __init__(self, index:int, value) -> None:
        super().__init__(index, "Operator", value)


class OpenParen(Operator):
    def __init__(self, index: int, value) -> None:
        super().__init__(index, value)

class CloseParen(Operator):
    def __init__(self, index: int, value) -> None:
        super().__init__(index, value)
    

class UnaryOperator(Operator):
    def __init__(self, index:int, value:str, operand:Token = None) -> None:
        super().__init__(index, value)
        self.operand = operand


class BinaryOperator(Operator):
    def __init__(self, index:int, value:str, left:Token = None, right:Token = None) -> None:
        super().__init__(index, value)
        self.left = left
        self.right = right

        
class Factorial(UnaryOperator):
    def __init__(self, index:int, value: str, operand: Token = None) -> None:
        super().__init__(index, value, operand)

    def evaluate(self) -> float:
        # Evaluate the operand
        value = self.operand.evaluate()

        # If the value is not a natural number, raise an exception
        if not(value >= 0 and value % 1 == 0):
            raise InvalidOperandException("Invalid operand for the factorial operator. Only natural numbers are allowed")

        # Else, evaluate the expression
        return self._factorial(value)

    def _factorial(self, n:int) -> int:
        if n == 0: return 1
        return n * self._factorial(n-1)


class Tilda(UnaryOperator):
    def __init__(self, index:int, value: str, operand: Token = None) -> None:
        super().__init__(index, value, operand)

    def evaluate(self) -> float:
        # If the operand is consist non-numbers tokens, raise an exception
        if not self._check_children(self.operand):
            raise InvalidOperandException("Invalid operand for the tilda operator. Only numbers are allowed, and not expressions")
        return -1 * self.operand.evaluate()

    def _check_children(self, node):
        # Base case: if the current node is null or a number, return true
        if not node or type(node) == Number:
            return True

        # If the node is not a negative token and not a number, return False
        if type(node) != Negative:
            return False
        
        # Check the rest of the nodes
        return self._check_children(node.operand)


class Negative(UnaryOperator):
    def __init__(self, index:int, value: str, operand: Token = None) -> None:
        super().__init__(index, value, operand)

    def evaluate(self) -> float:
        return -1 * self.operand.evaluate()


class SumDigits(UnaryOperator):
    def __init__(self, index:int, value: str, operand: Token = None) -> None:
        super().__init__(index, value, operand)

    def evaluate(self) -> float:
        # Evaluate the operand
        value = self.operand.evaluate()

        # If the operand it negative, raise an exception
        if value < 0:
            raise InvalidOperandException("Invalid operand for sum-digits operaor. Only non-negative numbers are allowed")
        return self._count_digits(value)

    def _count_digits(self, num):
        sum = 0
        for digit in str(num):
            if digit != '.':
                sum += int(digit)

        return sum

class Plus(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() + self.right.evaluate()


class Minus(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() - self.right.evaluate()


class Mult(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        return self.left.evaluate() * self.right.evaluate()


class Div(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        # Evaluate the operands
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()

        # If the right operand is 0, raise an exception
        if right_value == 0:
            raise InvalidOperandException("Invalid operand for division operator. Cannot divide by 0")
        
        # Else, evaluate the expression
        return left_value / right_value


class Power(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        # Evaluate the operands
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()

        # If the expression is 0^0, raise an exception
        if left_value == 0 and right_value == 0:
            raise InvalidOperandException("Invalid operand for power expression. Cannot evaluate 0^0")
        
        # Else, evaluate the expression
        return left_value ** right_value


class Mod(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        # Evaluate the operands
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()

        # If the right side is 0, raise an exception
        if right_value == 0:
            raise InvalidOperandException("Invalid operand for mod operator. Cannot divide by 0")
        return left_value % right_value


class Max(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        
        a = self.left.evaluate()
        b = self.right.evaluate()

        return a if a > b else b


class Min(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        
        a = self.left.evaluate()
        b = self.right.evaluate()

        return a if a < b else b


class Avg(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, index, value, left, right)

    def evaluate(self) -> float:        
        return (self.left.evaluate() + self.right.evaluate()) / 2

