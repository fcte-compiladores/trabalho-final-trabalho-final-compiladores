# --- Classe Base para Nós da AST ---
class ASTNode:
    def __init__(self, token=None):
        self.token = token # Opcional: armazena o token que gerou este nó

    def accept(self, visitor):
        """Permite que um visitor (como o interpretador) processe este nó."""
        method_name = 'visit_' + self.__class__.__name__
        visitor_method = getattr(visitor, method_name, None)
        if visitor_method:
            return visitor_method(self)
        else:
            raise NotImplementedError(f"Método visit_{self.__class__.__name__} não implementado no visitor.")

    def __repr__(self):
        # Para depuração simples, pode ser estendido em subclasses
        return self.__class__.__name__

# --- Nodos de Expressões ---
class Expression(ASTNode):
    pass

class BinaryExpression(Expression):
    def __init__(self, left: Expression, operator_token, right: Expression):
        super().__init__(operator_token)
        self.left = left
        self.operator = operator_token
        self.right = right

    def __repr__(self):
        return f"({repr(self.left)} {self.operator.value} {repr(self.right)})"

class UnaryExpression(Expression):
    def __init__(self, operator_token, right: Expression):
        super().__init__(operator_token)
        self.operator = operator_token
        self.right = right

    def __repr__(self):
        return f"({self.operator.value}{repr(self.right)})"

class NumberLiteral(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.value = int(token.value)

    def __repr__(self):
        return f"{self.value}"

class StringLiteral(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.value = token.value

    def __repr__(self):
        return f"'{self.value}'"

class Identifier(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.name = token.value

    def __repr__(self):
        return f"ID('{self.name}')"

# --- Nodos de Declarações (Statements) ---
class Statement(ASTNode):
    pass

class Program(ASTNode):
    def __init__(self, statements: list[Statement]):
        self.statements = statements

    def __repr__(self):
        return "\n".join(repr(s) for s in self.statements)

class VarDeclaration(Statement):
    def __init__(self, name_token, value: Expression):
        super().__init__(name_token)
        self.name = name_token
        self.value = value

    def __repr__(self):
        return f"VAR {self.name.value} = {repr(self.value)};"

class AssignmentStatement(Statement):
    def __init__(self, name_token, value: Expression):
        super().__init__(name_token)
        self.name = name_token
        self.value = value

    def __repr__(self):
        return f"SET {self.name.value} = {repr(self.value)};"

class MoveStatement(Statement):
    def __init__(self, direction_token, steps: Expression):
        super().__init__(direction_token)
        self.direction = direction_token
        self.steps = steps

    def __repr__(self):
        return f"MOVER {self.direction.value} {repr(self.steps)};"

class RotateStatement(Statement):
    def __init__(self, direction_token):
        super().__init__(direction_token)
        self.direction = direction_token

    def __repr__(self):
        return f"GIRAR {self.direction.value};"

class PickUpStatement(Statement):
    def __init__(self, token=None):
        super().__init__(token)

    def __repr__(self):
        return "PEGAR;"

class DropStatement(Statement):
    def __init__(self, token=None):
        super().__init__(token)

    def __repr__(self):
        return "SOLTAR;"

class PrintStatement(Statement):
    def __init__(self, expression: Expression):
        super().__init__()
        self.expression = expression

    def __repr__(self):
        return f"IMPRIMIR {repr(self.expression)};"

class IfStatement(Statement):
    def __init__(self, condition: Expression, then_block: list[Statement], else_block: list[Statement] = None):
        super().__init__()
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        then_str = "{" + "; ".join(repr(s) for s in self.then_block) + "}"
        else_str = ""
        if self.else_block:
            else_str = " SENAO {" + "; ".join(repr(s) for s in self.else_block) + "}"
        return f"SE ({repr(self.condition)}) ENTAO {then_str}{else_str}"

class RepeatStatement(Statement):
    def __init__(self, times: Expression, body: list[Statement]):
        super().__init__()
        self.times = times
        self.body = body

    def __repr__(self):
        body_str = "{" + "; ".join(repr(s) for s in self.body) + "}"
        return f"REPETIR {repr(self.times)} VEZES {body_str}"

# --- Bloco de comandos (para SE/SENAO/REPETIR) ---
class Block(ASTNode):
    def __init__(self, statements: list[Statement]):
        self.statements = statements
    
    def __repr__(self):
        return "{\n" + "\n".join(f"  {repr(s)}" for s in self.statements) + "\n}"