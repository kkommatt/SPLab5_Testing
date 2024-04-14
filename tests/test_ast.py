import pytest
from graphviz import Digraph

from AST.ast import draw_ast
from AST.ast_node import BinOpNode, NumNode, VarNode
from AST.new_parser import new_parser


@pytest.fixture
def setup_ast_node():
    yield


def test_bin_op_node(setup_ast_node):
    bin_op_node = BinOpNode(NumNode(10), '+', NumNode(5))

    assert isinstance(bin_op_node.left, NumNode)
    assert bin_op_node.operator == '+'
    assert isinstance(bin_op_node.right, NumNode)
    assert bin_op_node.left.value == 10
    assert bin_op_node.right.value == 5


def test_num_node(setup_ast_node):
    num_node = NumNode(10)

    assert num_node.value == 10


def test_var_node(setup_ast_node):
    var_node = VarNode('x')

    assert var_node.name == 'x'


# Fixture setup
@pytest.fixture
def setup_new_parser():
    yield


def test_parse_binop_node(setup_new_parser):
    input_string = "10+5"

    result = new_parser.parse(input_string)

    assert isinstance(result, BinOpNode)
    assert isinstance(result.left, NumNode)
    assert result.operator == '+'
    assert isinstance(result.right, NumNode)
    assert result.left.value == 10
    assert result.right.value == 5


def test_parse_num_node(setup_new_parser):
    input_string = "10"

    result = new_parser.parse(input_string)

    assert isinstance(result, NumNode)
    assert result.value == 10


def test_parse_var_node(setup_new_parser):
    input_string = "x"

    result = new_parser.parse(input_string)

    assert isinstance(result, VarNode)
    assert result.name == 'x'


@pytest.fixture
def setup_ast():
    yield


def test_draw_ast_binop(setup_ast):
    ast = "10 + 5"

    graph = draw_ast(ast)

    assert isinstance(graph, Digraph)
    assert "10" in graph.source
    assert "+" in graph.source
    assert "5" in graph.source


def test_draw_ast_num_node(setup_ast):
    ast = "10"

    # Draw the AST
    graph = draw_ast(ast)
    assert isinstance(graph, Digraph)
    assert "10" in graph.source


def test_draw_ast_var_node(setup_ast):
    ast = "x"

    graph = draw_ast(ast)

    assert isinstance(graph, Digraph)
    assert "x" in graph.source


def test_draw_ast_binop_nested(setup_ast):
    ast = "10+(5*3)"

    graph = draw_ast(ast)

    assert isinstance(graph, Digraph)
    assert "10" in graph.source
    assert "+" in graph.source
    assert "*" in graph.source
    assert "5" in graph.source
    assert "3" in graph.source


def test_draw_ast_complex_expression(setup_ast):
    ast = "(x+y)*(z-2)"

    graph = draw_ast(ast)

    # Assert statements
    assert isinstance(graph, Digraph)
    assert "+" in graph.source
    assert "-" in graph.source
    assert "x" in graph.source
    assert "y" in graph.source
    assert "z" in graph.source
    assert "2" in graph.source


@pytest.mark.parametrize("input_string", [
    "10 + 5",
    "7 - 3",
    "3 * 4",
    "6 / 2"
])
def test_draw_ast(setup_ast, input_string):
    graph = draw_ast(input_string)

    assert isinstance(graph, Digraph)
    assert [element in graph.source for element in input_string.split(' ')]
