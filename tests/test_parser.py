import pytest

from Parser import lex
from Parser.yacc_grammar import parser, variables


@pytest.fixture
def setup_lexer():
    yield


def test_identifier_tokenization(setup_lexer):
    input_string = "var1 _variable var_2"
    expected_token_types = ['IDENTIFIER', 'IDENTIFIER', 'IDENTIFIER']
    lex.lexer.input(input_string)
    actual_token_types = [token.type for token in lex.lexer]

    assert actual_token_types == expected_token_types


def test_number_tokenization(setup_lexer):
    input_string = "123 456.789"
    expected_token_types = ['NUMBER', 'NUMBER']

    lex.lexer.input(input_string)
    actual_token_types = [token.type for token in lex.lexer]

    assert actual_token_types == expected_token_types


def test_operator_tokenization(setup_lexer):
    input_string = "+ - * / ^"
    expected_token_types = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EXPONENT']

    lex.lexer.input(input_string)
    actual_token_types = [token.type for token in lex.lexer]

    assert actual_token_types == expected_token_types


def test_error_handling(setup_lexer):
    input_string = "@"
    with pytest.raises(ValueError):
        lex.lexer.input(input_string)
        token = lex.lexer.token()


@pytest.mark.parametrize("input_string, expected_token_types", [
    ("x=10+5", ['IDENTIFIER', 'EQUALS', 'NUMBER', 'PLUS', 'NUMBER']),
    ("(x+y)*2", ['LPAREN', 'IDENTIFIER', 'PLUS', 'IDENTIFIER', 'RPAREN', 'TIMES', 'NUMBER'])
])
def test_parameterized_tokenization(setup_lexer, input_string, expected_token_types):
    lex.lexer.input(input_string)
    actual_token_types = [token.type for token in lex.lexer]

    assert actual_token_types == expected_token_types


@pytest.fixture
def setup_parser():
    yield


def test_parse_assignment(setup_parser):
    input_string = "x = 10"

    result = parser.parse(input_string)

    assert variables['x'] == 10
    assert result == 10


def test_parse_expression(setup_parser):
    input_string = "10 + 5"

    result = parser.parse(input_string)

    assert result == 15


def test_parse_invalid_input(setup_parser):
    input_string = "x=10+"
    with pytest.raises(SyntaxError):
        parser.parse(input_string)


@pytest.mark.parametrize("input_string, expected_result", [
    ("x=10", 10),
    ("y=5*2", 10),
    ("z=x+y", 20)
])
def test_parameterized_parse_assignment(setup_parser, input_string, expected_result):
    result = parser.parse(input_string)

    variable_name = input_string.split('=')[0].strip()

    assert variables[variable_name] == expected_result
    assert result == expected_result





