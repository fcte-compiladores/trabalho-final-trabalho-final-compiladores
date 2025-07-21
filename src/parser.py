from src.lexer import TokenType, Token
from src.ast_nodes import (
    Program, Statement, Expression, BinaryExpression, UnaryExpression,
    NumberLiteral, StringLiteral, Identifier, VarDeclaration, AssignmentStatement,
    MoveStatement, RotateStatement, PickUpStatement, DropStatement,
    PrintStatement, IfStatement, RepeatStatement, Block
)

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def _advance(self):
        """Avança para o próximo token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = Token(TokenType.EOF, '', -1, -1) # Sentinel EOF

    def _eat(self, token_type: TokenType):
        """Verifica se o token atual é do tipo esperado e avança."""
        if self.current_token.type == token_type:
            token = self.current_token
            self._advance()
            return token
        else:
            self._error(f"Erro sintático: Esperava-se '{token_type.name}', mas encontrou '{self.current_token.type.name}' ('{self.current_token.value}') na linha {self.current_token.line}, coluna {self.current_token.column}.")

    def _error(self, message):
        """Lança um erro sintático."""
        raise Exception(message)

    def parse(self) -> Program:
        """Ponto de entrada do parser: retorna o nó raiz da AST (Program)."""
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self._statement())
        return Program(statements)

    def _statement(self) -> Statement:
        """Analisa uma declaração."""
        if self.current_token.type == TokenType.VAR:
            return self._var_declaration()
        elif self.current_token.type == TokenType.SET:
            return self._assignment_statement()
        elif self.current_token.type == TokenType.MOVER:
            return self._move_statement()
        elif self.current_token.type == TokenType.GIRAR:
            return self._rotate_statement()
        elif self.current_token.type == TokenType.PEGAR:
            return self._pickup_statement()
        elif self.current_token.type == TokenType.SOLTAR:
            return self._drop_statement()
        elif self.current_token.type == TokenType.IMPRIMIR:
            return self._print_statement()
        elif self.current_token.type == TokenType.SE:
            return self._if_statement()
        elif self.current_token.type == TokenType.REPETIR:
            return self._repeat_statement()
        else:
            self._error(f"Declaração inesperada: '{self.current_token.type.name}' na linha {self.current_token.line}, coluna {self.current_token.column}.")

    def _var_declaration(self) -> VarDeclaration:
        """VAR <id> = <expr>;"""
        self._eat(TokenType.VAR)
        name_token = self._eat(TokenType.IDENTIFICADOR)
        self._eat(TokenType.IGUAL)
        value_expr = self._expression()
        self._eat(TokenType.PONTO_VIRGULA)
        return VarDeclaration(name_token, value_expr)

    def _assignment_statement(self) -> AssignmentStatement:
        """SET <id> = <expr>;"""
        self._eat(TokenType.SET)
        name_token = self._eat(TokenType.IDENTIFICADOR)
        self._eat(TokenType.IGUAL)
        value_expr = self._expression()
        self._eat(TokenType.PONTO_VIRGULA)
        return AssignmentStatement(name_token, value_expr)

    def _move_statement(self) -> MoveStatement:
        """MOVER (FRENTE | TRAS) <expr>;"""
        self._eat(TokenType.MOVER)
        direction_token = self.current_token
        if direction_token.type not in (TokenType.FRENTE, TokenType.TRAS):
            self._error(f"Direção inválida para MOVER: '{direction_token.value}' na linha {direction_token.line}.")
        self._advance()
        steps_expr = self._expression()
        self._eat(TokenType.PONTO_VIRGULA)
        return MoveStatement(direction_token, steps_expr)

    def _rotate_statement(self) -> RotateStatement:
        """GIRAR (ESQUERDA | DIREITA);"""
        self._eat(TokenType.GIRAR)
        direction_token = self.current_token
        if direction_token.type not in (TokenType.ESQUERDA, TokenType.DIREITA):
            self._error(f"Direção inválida para GIRAR: '{direction_token.value}' na linha {direction_token.line}.")
        self._advance()
        self._eat(TokenType.PONTO_VIRGULA)
        return RotateStatement(direction_token)

    def _pickup_statement(self) -> PickUpStatement:
        """PEGAR;"""
        pickup_token = self._eat(TokenType.PEGAR)
        self._eat(TokenType.PONTO_VIRGULA)
        return PickUpStatement(pickup_token)

    def _drop_statement(self) -> DropStatement:
        """SOLTAR;"""
        drop_token = self._eat(TokenType.SOLTAR)
        self._eat(TokenType.PONTO_VIRGULA)
        return DropStatement(drop_token)

    def _print_statement(self) -> PrintStatement:
        """IMPRIMIR <expr>;"""
        self._eat(TokenType.IMPRIMIR)
        expr = self._expression()
        self._eat(TokenType.PONTO_VIRGULA)
        return PrintStatement(expr)

    def _if_statement(self) -> IfStatement:
        """SE (<condicao>) ENTAO { <bloco> } [SENAO { <bloco> }];"""
        self._eat(TokenType.SE)
        self._eat(TokenType.PARENTESE_ESQ)
        condition = self._expression() # A condição é uma expressão que será avaliada como booleana
        self._eat(TokenType.PARENTESE_DIR)
        self._eat(TokenType.ENTAO)
        then_block = self._block()

        else_block = None
        if self.current_token.type == TokenType.SENAO:
            self._eat(TokenType.SENAO)
            else_block = self._block()

        return IfStatement(condition, then_block, else_block)

    def _repeat_statement(self) -> RepeatStatement:
        """REPETIR <expr> VEZES { <bloco> };"""
        self._eat(TokenType.REPETIR)
        times_expr = self._expression()
        self._eat(TokenType.VEZES)
        body_block = self._block()
        return RepeatStatement(times_expr, body_block)

    def _block(self) -> list[Statement]:
        """{ <statement>* }"""
        self._eat(TokenType.CHAVE_ESQ)
        statements = []
        while self.current_token.type != TokenType.CHAVE_DIR:
            statements.append(self._statement())
        self._eat(TokenType.CHAVE_DIR)
        return statements


    # --- Gramática para Expressões (Ordem de Precedência) ---
    def _expression(self) -> Expression:
        """expression : comparison"""
        return self._comparison()

    def _comparison(self) -> Expression:
        """comparison : additive ((== | != | < | > | <= | >=) additive)*"""
        node = self._additive()
        while self.current_token.type in (
            TokenType.IGUAL, TokenType.DIFERENTE, TokenType.MENOR,
            TokenType.MAIOR, TokenType.MENOR_IGUAL, TokenType.MAIOR_IGUAL
        ):
            op = self.current_token
            self._advance()
            node = BinaryExpression(node, op, self._additive())
        return node

    def _additive(self) -> Expression:
        """additive : multiplicative ((+ | -) multiplicative)*"""
        node = self._multiplicative()
        while self.current_token.type in (TokenType.OP_SOMA, TokenType.OP_SUB):
            op = self.current_token
            self._advance()
            node = BinaryExpression(node, op, self._multiplicative())
        return node

    def _multiplicative(self) -> Expression:
        """multiplicative : unary ((* | /) unary)*"""
        node = self._unary()
        while self.current_token.type in (TokenType.OP_MULT, TokenType.OP_DIV):
            op = self.current_token
            self._advance()
            node = BinaryExpression(node, op, self._unary())
        return node

    def _unary(self) -> Expression:
        """unary : (+ | -) unary | primary"""
        if self.current_token.type in (TokenType.OP_SOMA, TokenType.OP_SUB):
            op = self.current_token
            self._advance()
            return UnaryExpression(op, self._unary())
        return self._primary()

    def _primary(self) -> Expression:
        """primary : NUMERO_INTEIRO | STRING | IDENTIFICADOR | (expression)"""
        token = self.current_token
        if token.type == TokenType.NUMERO_INTEIRO:
            self._eat(TokenType.NUMERO_INTEIRO)
            return NumberLiteral(token)
        elif token.type == TokenType.STRING:
            self._eat(TokenType.STRING)
            return StringLiteral(token)
        elif token.type == TokenType.IDENTIFICADOR:
            self._eat(TokenType.IDENTIFICADOR)
            return Identifier(token)
        elif token.type == TokenType.PARENTESE_ESQ:
            self._eat(TokenType.PARENTESE_ESQ)
            expr = self._expression()
            self._eat(TokenType.PARENTESE_DIR)
            return expr
        else:
            self._error(f"Erro sintático: Expressão primária inesperada: '{token.value}' na linha {token.line}, coluna {token.column}.")