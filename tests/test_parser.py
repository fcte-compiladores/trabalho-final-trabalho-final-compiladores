import pytest
from src.lexer import Lexer, TokenType
from src.parser import Parser
from src.ast_nodes import (
    Program, VarDeclaration, AssignmentStatement, NumberLiteral, Identifier,
    MoveStatement, RotateStatement, PrintStatement, BinaryExpression, StringLiteral,
    IfStatement, RepeatStatement, PickUpStatement, DropStatement
)

# Helper para parser um código e retornar a AST
def parse_code(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

# Teste de declaração de variável
def test_var_declaration_parsing():
    code = 'VAR idade = 30;'
    ast = parse_code(code)

    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert isinstance(stmt, VarDeclaration)
    assert stmt.name.value == 'idade'
    assert isinstance(stmt.value, NumberLiteral)
    assert stmt.value.value == 30

# Teste de atribuição
def test_assignment_parsing():
    code = 'SET contador = contador + 1;'
    ast = parse_code(code)

    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert isinstance(stmt, AssignmentStatement)
    assert stmt.name.value == 'contador'
    assert isinstance(stmt.value, BinaryExpression)
    assert stmt.value.operator.type == TokenType.OP_SOMA
    assert isinstance(stmt.value.left, Identifier)
    assert stmt.value.left.name == 'contador'
    assert isinstance(stmt.value.right, NumberLiteral)
    assert stmt.value.right.value == 1

# Teste de comando MOVER
def test_move_statement_parsing():
    code = 'MOVER FRENTE 10;'
    ast = parse_code(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, MoveStatement)
    assert stmt.direction.type == TokenType.FRENTE
    assert isinstance(stmt.steps, NumberLiteral)
    assert stmt.steps.value == 10

# Teste de comando IMPRIMIR com string
def test_print_string_parsing():
    code = 'IMPRIMIR "Olá Mundo";'
    ast = parse_code(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, PrintStatement)
    assert isinstance(stmt.expression, StringLiteral)
    assert stmt.expression.value == 'Olá Mundo'

# Teste de comando SE-ENTAO
def test_if_then_statement_parsing():
    code = 'SE (1 == 1) ENTAO { IMPRIMIR "Verdadeiro"; }'
    ast = parse_code(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, IfStatement)
    assert isinstance(stmt.condition, BinaryExpression)
    assert stmt.condition.operator.type == TokenType.IGUAL
    assert len(stmt.then_block) == 1
    assert isinstance(stmt.then_block[0], PrintStatement)
    assert stmt.else_block is None

# Teste de comando REPETIR
def test_repeat_statement_parsing():
    code = 'REPETIR 5 VEZES { GIRAR DIREITA; }'
    ast = parse_code(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, RepeatStatement)
    assert isinstance(stmt.times, NumberLiteral)
    assert stmt.times.value == 5
    assert len(stmt.body) == 1
    assert isinstance(stmt.body[0], RotateStatement)

# Teste de erro sintático (missing semicolon)
def test_syntax_error_missing_semicolon():
    code = 'VAR x = 1' # Falta ;
    with pytest.raises(Exception, match="Erro sintático: Esperava-se 'PONTO_VIRGULA'*"):
        parse_code(code)

# Teste de erro sintático (invalid statement)
def test_syntax_error_invalid_statement():
    code = 'INVALIDO COMANDO;'
    with pytest.raises(Exception, match="Declaração inesperada: 'IDENTIFICADOR'*"):
        parse_code(code)

# Teste para PEGAR e SOLTAR
def test_pickup_drop_parsing():
    code = 'PEGAR; SOLTAR;'
    ast = parse_code(code)
    assert len(ast.statements) == 2
    assert isinstance(ast.statements[0], PickUpStatement)
    assert isinstance(ast.statements[1], DropStatement)