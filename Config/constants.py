from tokens import *

# Valid operators
OPERATORS = {
    '+':Plus,
    '-':Minus,
    '*':Mult,
    '/':Div,
    '^':Power,
    '%':Mod,
    '$':Max,
    '&':Min,
    '@':Avg,
    '~':Tilda,
    '!':Factorial,
    '#':SumDigits,
    '(':OpenParen,
    ')':CloseParen}


# Binary operators priorities
PRIORITIES = {
    1: [Plus, Minus],
    2: [Mult, Div],
    3: [Power],
    4: [Mod],
    5: [Max, Min, Avg],
}