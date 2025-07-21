import sys
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <caminho/para/seu/arquivo.robo>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)

    print(f"--- Executando RoboScript: {file_path} ---")

    # Análise Léxica
    lexer = Lexer(source_code)
    try:
        tokens = lexer.tokenize()
        # for token in tokens:
        #     print(token)
    except Exception as e:
        print(f"Erro Léxico: {e}")
        sys.exit(1)

    # Análise Sintática (Parsing)
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        # print("--- AST Gerada ---")
        # print(ast)
    except Exception as e:
        print(f"Erro Sintático: {e}")
        sys.exit(1)

    # Interpretação
    interpreter = Interpreter()
    try:
        interpreter.interpret(ast)
        print("--- Execução Concluída ---")
    except Exception as e:
        print(f"Erro de Execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()