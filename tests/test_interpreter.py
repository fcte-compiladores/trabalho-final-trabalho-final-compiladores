import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from unittest.mock import patch
import io

# Helper para executar um código e retornar a saída (e o estado final do interpretador)
def execute_code(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    
    # Captura a saída do print
    with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
        interpreter.interpret(ast)
        output = fake_stdout.getvalue()
    
    return output, interpreter # Retorna a saída e a instância do interpretador para verificar o estado

# Teste de execução básica e IMPRIMIR
def test_basic_execution_and_print():
    code = 'IMPRIMIR "Olá RoboScript!";'
    output, _ = execute_code(code)
    assert "[IMPRIMIR] Olá RoboScript!\n" in output

# Teste de declaração e atribuição de variáveis
def test_variable_declaration_and_assignment():
    code = '''
    VAR a = 10;
    SET a = a + 5;
    IMPRIMIR a;
    '''
    output, interpreter = execute_code(code)
    assert "[Simulação] VAR 'a' = 10\n" in output
    assert "[Simulação] SET 'a' = 15\n" in output
    assert "[IMPRIMIR] 15\n" in output
    assert interpreter.environment.get('a') == 15

# Teste de movimentos do robô
def test_robot_movement():
    code = '''
    MOVER FRENTE 5;
    GIRAR DIREITA;
    MOVER FRENTE 3;
    '''
    output, interpreter = execute_code(code)
    assert "[Simulação] Robo moveu FRENTE 5 passos. Posicao: (0,0) -> (0,5)\n" in output
    assert "[Simulação] Robo girou DIREITA. Direção: NORTE -> LESTE\n" in output
    assert "[Simulação] Robo moveu FRENTE 3 passos. Posicao: (0,5) -> (3,5)\n" in output
    assert interpreter.robot_x == 3
    assert interpreter.robot_y == 5
    assert interpreter.robot_direction == "LESTE"

# Teste de PEGAR e SOLTAR
def test_pickup_drop():
    code = '''
    PEGAR;
    SOLTAR;
    PEGAR;
    '''
    output, interpreter = execute_code(code)
    assert "[Simulação] Robo PEGOU um objeto na posicao (0,0).\n" in output
    assert "[Simulação] Robo SOLTOU um objeto na posicao (0,0).\n" in output
    assert "Robo já está segurando um objeto." not in output
    assert interpreter.has_object == True

# Teste de operadores aritméticos e concatenação de string
def test_arithmetic_and_string_concatenation():
    code = '''
    VAR num = 7;
    VAR texto = "O número é: ";
    IMPRIMIR texto + num;
    IMPRIMIR 10 * 2 + 5;
    '''
    output, _ = execute_code(code)
    assert "[IMPRIMIR] O número é: 7\n" in output
    assert "[IMPRIMIR] 25\n" in output

# Teste de condicionais (IF/ELSE)
def test_if_else_statement():
    code_if_true = '''
    VAR x = 10;
    SE (x > 5) ENTAO {
        IMPRIMIR "X é maior que 5";
    } SENAO {
        IMPRIMIR "X não é maior que 5";
    }
    '''
    output_true, _ = execute_code(code_if_true)
    assert "[IMPRIMIR] X é maior que 5\n" in output_true
    assert "X não é maior que 5" not in output_true

    code_if_false = '''
    VAR y = 3;
    SE (y > 5) ENTAO {
        IMPRIMIR "Y é maior que 5";
    } SENAO {
        IMPRIMIR "Y não é maior que 5";
    }
    '''
    output_false, _ = execute_code(code_if_false)
    assert "Y é maior que 5" not in output_false
    assert "[IMPRIMIR] Y não é maior que 5\n" in output_false

# Teste de loop REPETIR
def test_repeat_statement():
    code = '''
    VAR i = 0;
    REPETIR 3 VEZES {
        IMPRIMIR "Loop: " + i;
        SET i = i + 1;
    }
    '''
    output, _ = execute_code(code)
    assert "[IMPRIMIR] Loop: 0\n" in output
    assert "[IMPRIMIR] Loop: 1\n" in output
    assert "[IMPRIMIR] Loop: 2\n" in output
    assert "Loop: 3" not in output # Garante que não repetiu uma vez a mais

# Teste de acesso às variáveis de estado do robô
def test_robot_state_variables_access():
    code = '''
    IMPRIMIR robot_x;
    IMPRIMIR robot_y;
    IMPRIMIR robot_direction;
    MOVER FRENTE 1;
    IMPRIMIR robot_x;
    IMPRIMIR robot_y;
    PEGAR;
    IMPRIMIR has_object;
    '''
    output, _ = execute_code(code)
    assert "[IMPRIMIR] 0\n" in output # robot_x inicial
    assert "[IMPRIMIR] 0\n" in output # robot_y inicial
    assert "[IMPRIMIR] NORTE\n" in output # robot_direction inicial
    assert "[IMPRIMIR] 0\n" in output # robot_x após mover (continua em x=0)
    assert "[IMPRIMIR] 1\n" in output # robot_y após mover (agora é y=1)
    assert "[IMPRIMIR] 1\n" in output # has_object = True (representado como 1)

# Teste de erro de divisão por zero
def test_division_by_zero_error():
    code = 'IMPRIMIR 10 / 0;'
    with pytest.raises(Exception, match="Erro de Execução: Divisão por zero."):
        execute_code(code)

# Em tests/test_interpreter.py
def test_undefined_variable_error():
    code = 'IMPRIMIR z;'
    with pytest.raises(Exception, match="Erro de Execução: .*Variável 'z' não definida."):
        execute_code(code)

# Em tests/test_interpreter.py
def test_division_by_zero_error():
    code = 'IMPRIMIR 10 / 0;'
    with pytest.raises(Exception, match="Erro de Execução: .*Divisão por zero."):
        execute_code(code)