from Exceptions.exceptions import *


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

    # Method to validate the operands. Returns True by default (if not overridden)
    def validate_operands(self) -> bool:
        return True


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
        self.value = self.operand.evaluate()

        # Validate the operands
        if self.validate_operands():
            return self._factorial(self.value)

    def _factorial(self, n:int) -> int:
        if n == 0: return 1
        return n * self._factorial(n-1)

    def validate_operands(self) -> bool:
        
         # If the value is not a natural number, raise an exception
        if not(self.value >= 0 and self.value % 1 == 0):
            raise InvalidOperandException("Invalid operand for the factorial operator. Only natural numbers are allowed")
        
        # Else, return True
        return True


class Tilda(UnaryOperator):
    def __init__(self, index:int, value: str, operand: Token = None) -> None:
        super().__init__(index, value, operand)

    def evaluate(self) -> float:
        # Validate the operands
        if self.validate_operands():
            return -1 * self.operand.evaluate()

    def validate_operands(self) -> bool:
        # If the operand is consist non-numbers tokens, raise an exception
        if not self._check_children(self.operand):
            raise InvalidOperandException("Invalid operand for the tilda operator. Only numbers are allowed, and not expressions")

        # Else, return True
        return True

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
        return self._count_digits(self.operand.evaluate())

    def _count_digits(self, num):
        sum = 0
        for digit in str(num):
            if digit != '.' and digit != '-':
                sum += int(digit)

        return sum if num > 0 else -sum

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
        self.left_value = self.left.evaluate()
        self.right_value = self.right.evaluate() 
        
        # Validate the operands
        if self.validate_operands():
            return self.left_value / self.right_value

    def validate_operands(self) -> bool:
        # If the right operand is 0, raise an exception
        if self.right_value == 0:
            raise InvalidOperandException("Invalid operand for division operator. Cannot divide by 0")

        # Else, return True
        return True


class Power(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        # Evaluate the operands
        self.left_value = self.left.evaluate()
        self.right_value = self.right.evaluate()

        # Validate the operands
        if self.validate_operands():
            value = self.left_value ** self.right_value

        # If the value is a complex number, raise an exception
        if type(value) == complex:
            raise InvalidOperandException("Invalid operand for power expression. The result of the power expression is a complex number")

    def validate_operands(self) -> bool:
        # If the expression is 0^0, raise an exception
        if self.left_value == 0 and self.right_value == 0:
            raise InvalidOperandException("Invalid operand for power expression. Cannot evaluate 0^0")
        
        # Else, return True
        return True


class Mod(BinaryOperator):
    def __init__(self, index:int, value: str, left: Token = None, right: Token = None) -> None:
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:
        # Evaluate the operands
        self.left_value = self.left.evaluate()
        self.right_value = self.right.evaluate()

        # Validate the operands
        if self.validate_operands():
            return self.left_value % self.right_value

    def validate_operands(self) -> bool:
        # If the right side is 0, raise an exception
        if self.right_value == 0:
            raise InvalidOperandException("Invalid operand for mod operator. Cannot divide by 0")

        # Else, return True
        return True


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
        super().__init__(index, value, left, right)

    def evaluate(self) -> float:        
        return (self.left.evaluate() + self.right.evaluate()) / 2

