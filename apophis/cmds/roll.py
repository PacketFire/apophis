""" Roll Command """
from cmds.command import Command
from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Optional
from typing import Union
import random
import re


@dataclass
class Expression:
    value: Union['Dice', 'Constant', 'Add']


@dataclass
class Dice:
    rolls: int
    faces: int


@dataclass
class Constant:
    c: int


@dataclass
class Add:
    left: Expression
    right: Expression


def dice(rolls: int, faces: int) -> Expression:
    return Expression(Dice(rolls, faces))


def constant(c: int) -> Expression:
    return Expression(Constant(c))


def add(lhs: Expression, rhs: Expression) -> Expression:
    return Expression(Add(lhs, rhs))


def evaluate(expr: Expression) -> List[int]:
    value = expr.value
    if isinstance(value, Constant):
        return [value.c]
    elif isinstance(value, Dice):
        xs = list(range(value.rolls))
        return [random.randint(1, value.faces) for _ in xs]
    elif isinstance(value, Add):
        return evaluate(value.left) + evaluate(value.right)
    else:
        return []


@dataclass
class LexerRule:
    tag: str
    regex: str


@dataclass
class Token:
    tag: str
    text: str


@dataclass
class Result:
    token: Any
    tokens: List[Token]


integer_rule = LexerRule('integer', r'[0-9]+')
d_rule = LexerRule('d', r'd')
plus_rule = LexerRule('plus', r'\s*\+\s*')
lexer_rules = [integer_rule, d_rule, plus_rule]


def lex(input: str) -> Optional[List[Token]]:
    pos = 0
    tokens = []
    while pos < len(input):
        match = None
        for rule in lexer_rules:
            regex = re.compile(rule.regex)
            match = regex.match(input, pos)
            if match:
                text = match.group(0)
                token = Token(rule.tag, text)
                tokens.append(token)
                break
        if match:
            pos = match.end(0)
        else:
            return None

    return tokens


def parse_dice(tokens: List[Any]) -> Optional[Result]:
    if len(tokens) < 3:
        return None

    if tokens[0].tag != 'integer':
        return None

    if tokens[1].tag != 'd':
        return None

    if tokens[2].tag != 'integer':
        return None

    return Result(dice(int(tokens[0].text), int(tokens[2].text)), tokens[3:])


def parse_constant(tokens: List[Token]) -> Optional[Result]:
    if len(tokens) == 0:
        return None

    if tokens[0].tag == 'integer':
        return Result(constant(int(tokens[0].text)), tokens[1:])
    else:
        return None


def parse_term(tokens: List[Token]) -> Optional[Result]:
    dice = parse_dice(tokens)
    if dice is not None:
        return dice

    constant = parse_constant(tokens)
    if constant is not None:
        return constant

    return None


def parse_plus(tokens: List[Token]) -> Optional[Result]:
    if len(tokens) == 0:
        return None

    if tokens[0].tag == 'plus':
        return Result(None, tokens[1:])
    else:
        return None


def parse_addition(tokens: List[Token]) -> Optional[Result]:
    lhs = parse_term(tokens)
    if lhs is None:
        return None

    plus = parse_plus(lhs.tokens)
    if plus is None:
        return None

    rhs = parse_expression(plus.tokens)
    if rhs is None:
        return None

    return Result(add(lhs.token, rhs.token), rhs.tokens)


def parse_expression(tokens: List[Token]) -> Optional[Result]:
    addition = parse_addition(tokens)
    if addition is not None:
        return addition

    term = parse_term(tokens)
    if term is not None:
        return term

    return None


def parse(input: str) -> Optional[Expression]:
    tokens = lex(input)
    if tokens is None:
        return None

    parsed = parse_expression(tokens)
    if parsed is None:
        return None

    return parsed.token


class RollCommand(Command):
    async def handle(self, context, message):
        input = message.content[6:].strip()
        expression = parse(input)

        if expression is None:
            return await message.channel.send('Invalid roll expression.')
        else:
            terms = evaluate(expression)
            sum_string = ' + '.join(f'**{str(t)}**' for t in terms)

            return await message.channel.send(
                f'{sum_string} = **{sum(terms)}**'
            )
