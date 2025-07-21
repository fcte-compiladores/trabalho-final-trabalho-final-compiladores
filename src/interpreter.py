from src.ast_nodes import (
    Program, Statement, Expression, BinaryExpression, UnaryExpression,
    NumberLiteral, StringLiteral, Identifier, VarDeclaration, AssignmentStatement,
    MoveStatement, RotateStatement, PickUpStatement, DropStatement,
    PrintStatement, IfStatement, RepeatStatement, Block
)
from src.lexer import TokenType
from src.environment import Environment

class Interpreter:
    def __init__(self):
        self.environment = Environment()
        # Estado do robô (simulado)
        self.robot_x = 0
        self.robot_y = 0
        self.robot_direction = "NORTE" # NORTE, LESTE, SUL, OESTE
        self.has_object = False

    def _error(self, message, token=None):
        line_info = f"Linha {token.line}, coluna {token.column}: " if token else ""
        raise Exception(f"Erro de Execução: {line_info}{message}")

    def interpret(self, program: Program):
        for statement in program.statements:
            self.visit(statement)

    def visit(self, node):
        """Método dispatcher para o padrão Visitor."""
        if node is None:
            return None
        method_name = 'visit_' + type(node).__name__
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node):
        """Método de fallback para nós não implementados."""
        raise NotImplementedError(f"Método de visita não implementado para o nó: {type(node).__name__}")

    # --- Métodos de Visita para Declarações (Statements) ---
    def visit_Program(self, node: Program):
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDeclaration(self, node: VarDeclaration):
        value = self.visit(node.value)
        # Permite que variáveis sejam inicializadas com strings também
        # if not isinstance(value, int):
        #     self._error(f"Variável '{node.name.value}' deve ser inicializada com um número inteiro.", node.name)
        self.environment.define(node.name.value, value)
        print(f"[Simulação] VAR '{node.name.value}' = {value}")

    def visit_AssignmentStatement(self, node: AssignmentStatement):
        if not self.environment.exists(node.name.value):
            self._error(f"Variável '{node.name.value}' não declarada antes de ser atribuída.", node.name)
        value = self.visit(node.value)
        # Permite atribuição de strings também
        # if not isinstance(value, int):
        #     self._error(f"Valor atribuído a '{node.name.value}' deve ser um número inteiro.", node.name)
        self.environment.assign(node.name.value, value)
        print(f"[Simulação] SET '{node.name.value}' = {value}")

    def visit_MoveStatement(self, node: MoveStatement):
        steps = self.visit(node.steps)
        if not isinstance(steps, int) or steps < 0:
            self._error(f"Número de passos inválido: {steps}. Deve ser um inteiro positivo.", node.steps.token)

        old_x, old_y = self.robot_x, self.robot_y
        if node.direction.type == TokenType.FRENTE:
            if self.robot_direction == "NORTE": self.robot_y += steps
            elif self.robot_direction == "LESTE": self.robot_x += steps
            elif self.robot_direction == "SUL": self.robot_y -= steps
            elif self.robot_direction == "OESTE": self.robot_x -= steps
            print(f"[Simulação] Robo moveu FRENTE {steps} passos. Posicao: ({old_x},{old_y}) -> ({self.robot_x},{self.robot_y})")
        elif node.direction.type == TokenType.TRAS:
            if self.robot_direction == "NORTE": self.robot_y -= steps
            elif self.robot_direction == "LESTE": self.robot_x -= steps
            elif self.robot_direction == "SUL": self.robot_y += steps
            elif self.robot_direction == "OESTE": self.robot_x -= steps
            print(f"[Simulação] Robo moveu TRAS {steps} passos. Posicao: ({old_x},{old_y}) -> ({self.robot_x},{self.robot_y})")
        
    def visit_RotateStatement(self, node: RotateStatement):
        old_direction = self.robot_direction
        directions = ["NORTE", "LESTE", "SUL", "OESTE"]
        current_idx = directions.index(self.robot_direction)

        if node.direction.type == TokenType.DIREITA:
            self.robot_direction = directions[(current_idx + 1) % 4]
            print(f"[Simulação] Robo girou DIREITA. Direção: {old_direction} -> {self.robot_direction}")
        elif node.direction.type == TokenType.ESQUERDA:
            self.robot_direction = directions[(current_idx - 1 + 4) % 4]
            print(f"[Simulação] Robo girou ESQUERDA. Direção: {old_direction} -> {self.robot_direction}")

    def visit_PickUpStatement(self, node: PickUpStatement):
        if self.has_object:
            print("[Simulação] Robo já está segurando um objeto.")
        else:
            self.has_object = True
            print(f"[Simulação] Robo PEGOU um objeto na posicao ({self.robot_x},{self.robot_y}).")

    def visit_DropStatement(self, node: DropStatement):
        if not self.has_object:
            print("[Simulação] Robo não está segurando nenhum objeto para SOLTAR.")
        else:
            self.has_object = False
            print(f"[Simulação] Robo SOLTOU um objeto na posicao ({self.robot_x},{self.robot_y}).")

    def visit_PrintStatement(self, node: PrintStatement):
        value = self.visit(node.expression)
        print(f"[IMPRIMIR] {value}")

    def visit_IfStatement(self, node: IfStatement):
        condition_result = self.visit(node.condition)
        # Em RoboScript, 0 é falso, qualquer outro inteiro é verdadeiro. Ou podemos forçar booleanos.
        if isinstance(condition_result, bool): # Se sua expressão de comparação já retornar bool
            condition_is_true = condition_result
        elif isinstance(condition_result, int): # Se expressões retornam int
            condition_is_true = condition_result != 0
        else:
            self._error(f"Condição do 'SE' deve ser avaliada como booleano ou inteiro (0 para falso): {condition_result}", node.condition.token)


        if condition_is_true:
            for statement in node.then_block:
                self.visit(statement)
        elif node.else_block:
            for statement in node.else_block:
                self.visit(statement)

    def visit_RepeatStatement(self, node: RepeatStatement):
        times = self.visit(node.times)
        if not isinstance(times, int) or times < 0:
            self._error(f"Número de repetições inválido: {times}. Deve ser um inteiro não negativo.", node.times.token)
        
        for _ in range(times):
            for statement in node.body:
                self.visit(statement)

    # --- Métodos de Visita para Expressões (Expressions) ---
    def visit_NumberLiteral(self, node: NumberLiteral):
        return node.value

    def visit_StringLiteral(self, node: StringLiteral):
        return node.value

    def visit_Identifier(self, node: Identifier):
        # Primeiro, verifica se é uma variável de estado do robô
        if node.name == "robot_x":
            return self.robot_x
        if node.name == "robot_y":
            return self.robot_y
        if node.name == "robot_direction":
            return self.robot_direction
        if node.name == "has_object":
            return 1 if self.has_object else 0 # Retorna 1 para True, 0 para False

        # Se não for uma variável de estado do robô, busca no ambiente normal
        try:
            value = self.environment.get(node.name)
            return value
        except ValueError as e: # Captura o erro do ambiente
            self._error(str(e), node.token) # E formata usando o _error do interpreter

    def visit_BinaryExpression(self, node: BinaryExpression):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        op_type = node.operator.type

        # Lógica para concatenação de strings com o operador '+'
        if op_type == TokenType.OP_SOMA:
            if isinstance(left_val, str) or isinstance(right_val, str):
                # Se um dos operandos for string, converte o outro para string e concatena
                return str(left_val) + str(right_val)
            else:
                # Caso contrário, realiza adição numérica
                return left_val + right_val
        elif op_type == TokenType.OP_SUB:
            return left_val - right_val
        elif op_type == TokenType.OP_MULT:
            return left_val * right_val
        elif op_type == TokenType.OP_DIV:
            if right_val == 0:
                self._error("Divisão por zero.", node.operator)
            return left_val // right_val # Divisão inteira
        elif op_type == TokenType.IGUAL:
            return left_val == right_val
        elif op_type == TokenType.DIFERENTE:
            return left_val != right_val
        elif op_type == TokenType.MENOR:
            return left_val < right_val
        elif op_type == TokenType.MAIOR:
            return left_val > right_val
        elif op_type == TokenType.MENOR_IGUAL:
            return left_val <= right_val
        elif op_type == TokenType.MAIOR_IGUAL:
            return left_val >= right_val
        else:
            self._error(f"Operador binário desconhecido: {node.operator.value}", node.operator)

    def visit_UnaryExpression(self, node: UnaryExpression):
        right_val = self.visit(node.right)
        op_type = node.operator.type
        if op_type == TokenType.OP_SUB: # Negativo
            return -right_val
        elif op_type == TokenType.OP_SOMA: # Positivo (sem efeito)
            return +right_val
        else:
            self._error(f"Operador unário desconhecido: {node.operator.value}", node.operator)
