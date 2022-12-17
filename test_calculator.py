import pytest

from lexer import Lexer
from parsing import RecursiveDescentParser
from Exceptions.exceptions import *


def calculate(string:str):
    lexer = Lexer()
    parser = RecursiveDescentParser()
    
    tokens = lexer.lex(string)
    result = parser.parse(tokens, string).evaluate()

    return result


# Simple syntax errors
def test_missing_operator_1():
    # missing operator between the 3 and the (34-20)
    string = "3(34-20)\0"
    with pytest.raises(MissingOperatorException):
        calculate(string)

def test_missing_operator_2():
    # missing operator between the 3! and the 20
    string = "3!20-30\0"
    with pytest.raises(MissingOperatorException):
        calculate(string)

def test_missing_operand():
    # missing operand between the + and the *
    string = "130+*3\0"
    with pytest.raises(MissingOperandException):
        calculate(string)

def test_missing_paren_1():
    # missing closing paren
    string = "((10-23)+3!\0"
    with pytest.raises(MissingParenthesisException):
        calculate(string)

def test_missing_paren_1():
    # missing opening paren
    string = "((10-23)))+3!\0"
    with pytest.raises(MissingParenthesisException):
        calculate(string)


# Nonsense strings
def test_nonsence():
    # = is an invalid character
    string = "14 + 23 = 12\0"
    with pytest.raises(InvalidSymbolException):
        calculate(string)

# Empty string
def test_empty_string():
    # an empty string
    string = "\0"
    with pytest.raises(EmptyInputString):
        calculate(string)
    
# Whitespaced characters
def test_whitespace_string():
    # a string that contains whitespaces only
    string = "   \t\r\0"
    with pytest.raises(EmptyInputString):
        calculate(string)


# Simple equations to test operators seperately
def test_addition_operator():
    string = "3+2\0"
    assert calculate(string) == 5

def test_subtraction_operator():
    string = "100-54\0"
    assert calculate(string) == 46

def test_multiplication_operator():
    string = "3*21\0"
    assert calculate(string) == 63

def test_division_operator():
    string = "15/2\0"
    assert calculate(string) == 7.5

def test_power_operator():
    string = "-2^3\0"
    assert calculate(string) == -8

def test_mod_operator():
    string = "19%7\0"
    assert calculate(string) == 5

def test_max_operator():
    string = "4$10\0"
    assert calculate(string) == 10

def test_min_operator():
    string = "3&2\0"
    assert calculate(string) == 2

def test_avg_operator():
    string = "12@20\0"
    assert calculate(string) == 16

def test_tilda_operator():
    string = "~--2\0"
    assert calculate(string) == -2

def test_factorial_operator():
    string = "5!\0"
    assert calculate(string) == 120

def test_sum_digits_operator():
    string = "15364#\0"
    assert calculate(string) == 19



# Valid complex equations
def test_complex_equation_1():
    string = "(3*(5-2)!)/((5!)/((-2^2)!)+1)\0"
    assert calculate(string) == 3

def test_complex_equation_2():
    string = "((5&2)^(2^2$-4)- 3!)*-(-2@5!#!)\0"
    assert calculate(string) == -20

def test_complex_equation_3():
    string = "4!#^ 2 -(2^(-(2^2)@(2^3)))!\0"
    assert calculate(string) == 12

def test_complex_equation_4():
    string = "((22/2)^2)#! - ~---120#!\0"
    assert calculate(string) == 18

def test_complex_equation_5():
    string = "(10*(5@15))@((15%4)^(2^2))\0"
    assert calculate(string) == 90.5

def test_complex_equation_6():
    string = "((7!/6!)^2+1)- (40@((4*5)$60))\0"
    assert calculate(string) == 0

def test_complex_equation_7():
    string = "(19%(4!/4)+2)^(~---2! + 2^3 - (4^2)/2)\0"
    assert calculate(string) == 9

def test_complex_equation_8():
    string = "((7 *(2^2))/2)@(5*(((3^2)*2)/6))\0"
    assert calculate(string) == 14.5

def test_complex_equation_9():
    string = "((7*3+2)#^-(-2&5)*2)*(5*2-4!#)\0"
    assert calculate(string) == 200

def test_complex_equation_10():
    string = "((2*2*2)*3!)-(((20^2)/2)/20)*6\0"
    assert calculate(string) == -12

def test_complex_equation_11():
    string = "(4!/2^3)^2+2^((20+6@(2^3))/3^2)\0"
    assert calculate(string) == 17

def test_complex_equation_12():
    string = "(6*3+1@(6^2/(2^2*3)))/(6!#-(8*5+1)#)\0"
    assert calculate(string) == 5

def test_complex_equation_13():
    string = "(11^2)%((10+1!#)*((5*2^1)&(5*2^2)))\0"
    assert calculate(string) == 11

def test_complex_equation_14():
    string = "42%(6!#-(2^2*2^3+10)%(2^3+5&12))\0"
    assert calculate(string) == 0

def test_complex_equation_15():
    string = "-(2^3)*(5!#+3)+((5^2*2^2)/10+~---4)\0"
    assert calculate(string) == -34

def test_complex_equation_16():
    string = "-((5+5+150%(40*3))*2@3)-(7*2^(11%(2^1*2^2)))\0"
    assert calculate(string) == -156

def test_complex_equation_17():
    string = "-((10$4*3)*2^2+(25%(3*5)))+(20-(2^2)@(2*3))\0"
    assert calculate(string) == -115

def test_complex_equation_18():
    string = "(30$14)*120#+2^(2&10)-(0.5+1/(16%((5!+1)/11)))\0"
    assert calculate(string) == 93.3

def test_complex_equation_19():
    string = "50*(0.04*10^2)+3-2^(~--5@(10+(10*10)#))\0"
    assert calculate(string) == 195

def test_complex_equation_20():
    string = "((10+10+10+3^2)/5!#)^2-(0.5*(2^-(-2&2)))\0"
    assert calculate(string) == 167