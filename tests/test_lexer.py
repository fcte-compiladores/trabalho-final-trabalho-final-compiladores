import pytest
from src.lexer import Lexer, TokenType, Token

# Teste básico para comandos e literais
def test_basic_commands_and_literals():
    code = 'IMPRIMIR "Olá Mundo"; MOVER FRENTE 10;'
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    expected_tokens = [
        Token(TokenType.IMPRIMIR, "IMPRIMIR", 1, 1),
        Token(TokenType.STRING, "Olá Mundo", 1, 10),
        Token(TokenType.PONTO_VIRGULA, ";", 1, 21),
        Token(TokenType.MOVER, "MOVER", 1, 23),
        Token(TokenType.FRENTE, "FRENTE", 1, 29),
        Token(TokenType.NUMERO_INTEIRO, "10", 1, 36),
        Token(TokenType.PONTO_VIRGULA, ";", 1, 38),
        Token(TokenType.EOF, "", 1, 39)
    ]
    
    assert [t.type for t in tokens] == [t.type for t in expected_tokens]
    assert [t.value for t in tokens] == [t.value for t in expected_tokens]

# Teste de variáveis e atribuição
def test_variables_and_assignment():
    code = 'VAR x = 5; SET y = x + 2;'
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    expected_types = [
        TokenType.VAR, TokenType.IDENTIFICADOR, TokenType.IGUAL, TokenType.NUMERO_INTEIRO, TokenType.PONTO_VIRGULA,
        TokenType.SET, TokenType.IDENTIFICADOR, TokenType.IGUAL, TokenType.IDENTIFICADOR, TokenType.OP_SOMA, TokenType.NUMERO_INTEIRO, TokenType.PONTO_VIRGULA,
        TokenType.EOF
    ]
    assert [t.type for t in tokens] == expected_types

# Teste de operadores complexos e parênteses
def test_operators_and_parentheses():
    code = 'resultado = (10 + 5) * 2 / (4 - 1);'
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    expected_types = [
        TokenType.IDENTIFICADOR, TokenType.IGUAL, 
        TokenType.PARENTESE_ESQ, TokenType.NUMERO_INTEIRO, TokenType.OP_SOMA, TokenType.NUMERO_INTEIRO, TokenType.PARENTESE_DIR,
        TokenType.OP_MULT, TokenType.NUMERO_INTEIRO, TokenType.OP_DIV, 
        TokenType.PARENTESE_ESQ, TokenType.NUMERO_INTEIRO, TokenType.OP_SUB, TokenType.NUMERO_INTEIRO, TokenType.PARENTESE_DIR,
        TokenType.PONTO_VIRGULA,
        TokenType.EOF
    ]
    assert [t.type for t in tokens] == expected_types

# Teste de comentários
def test_comments():
    code = '''
    // Este é um comentário
    VAR a = 1; // Outro comentário
    IMPRIMIR "Fim";
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    expected_types = [
        TokenType.VAR, TokenType.IDENTIFICADOR, TokenType.IGUAL, TokenType.NUMERO_INTEIRO, TokenType.PONTO_VIRGULA,
        TokenType.IMPRIMIR, TokenType.STRING, TokenType.PONTO_VIRGULA,
        TokenType.EOF
    ]
    assert [t.type for t in tokens] == expected_types


def test_lexical_error():
    code = 'VAR x = #erro;'
    lexer = Lexer(code)
    with pytest.raises(Exception, match=r"Erro léxico na linha \d+, coluna \d+: Caractere inesperado: '#'\.?"):

        lexer.tokenize()

# Teste de strings não terminadas (exemplo para erro)
def test_unterminated_string():
    code = 'IMPRIMIR "string sem fim;'
    lexer = Lexer(code)
    with pytest.raises(Exception, match=r'Erro léxico na linha \d+, coluna \d+: String não terminada\. Esperava-se \'"\'\.'):
        lexer.tokenize()
