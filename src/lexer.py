from enum import Enum, auto

# --- Definição dos Tipos de Tokens ---
class TokenType(Enum):
    # Palavras-chave
    VAR = auto()
    SET = auto()
    MOVER = auto()
    FRENTE = auto()
    TRAS = auto()
    GIRAR = auto()
    ESQUERDA = auto()
    DIREITA = auto()
    PEGAR = auto()
    SOLTAR = auto()
    IMPRIMIR = auto()
    SE = auto()
    ENTAO = auto()
    SENAO = auto()
    REPETIR = auto()
    VEZES = auto()

    # Operadores
    IGUAL = auto()       # =
    OP_SOMA = auto()     # +
    OP_SUB = auto()      # -
    OP_MULT = auto()     # *
    OP_DIV = auto()      # /
    MAIOR = auto()       # >
    MENOR = auto()       # <
    MAIOR_IGUAL = auto() # >=
    MENOR_IGUAL = auto() # <=
    DIFERENTE = auto()   # !=

    # Símbolos
    PARENTESE_ESQ = auto() # (
    PARENTESE_DIR = auto() # )
    CHAVE_ESQ = auto()     # {
    CHAVE_DIR = auto()     # }
    PONTO_VIRGULA = auto() # ;
    VIRGULA = auto()       # ,
    ASPAS = auto()         # "

    # Literais e Identificadores
    NUMERO_INTEIRO = auto()
    STRING = auto()
    IDENTIFICADOR = auto()

    # Outros
    EOF = auto() # End Of File

# --- Classe Token ---
class Token:
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token(Type: {self.type.name}, Value: '{self.value}', Line: {self.line}, Col: {self.column})"

    def __repr__(self):
        return self.__str__()

# --- Classe Lexer ---
class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.current_char = self.source[self.position] if self.source else None
        self.line = 1
        self.column = 1
        self.tokens = []

        # Mapeamento de palavras-chave
        self.keywords = {
            "VAR": TokenType.VAR,
            "SET": TokenType.SET,
            "MOVER": TokenType.MOVER,
            "FRENTE": TokenType.FRENTE,
            "TRAS": TokenType.TRAS,
            "GIRAR": TokenType.GIRAR,
            "ESQUERDA": TokenType.ESQUERDA,
            "DIREITA": TokenType.DIREITA,
            "PEGAR": TokenType.PEGAR,
            "SOLTAR": TokenType.SOLTAR,
            "IMPRIMIR": TokenType.IMPRIMIR,
            "SE": TokenType.SE,
            "ENTAO": TokenType.ENTAO,
            "SENAO": TokenType.SENAO,
            "REPETIR": TokenType.REPETIR,
            "VEZES": TokenType.VEZES,
        }

    def _advance(self):
        """Avança para o próximo caractere."""
        self.position += 1
        self.column += 1
        if self.position < len(self.source):
            self.current_char = self.source[self.position]
        else:
            self.current_char = None

    def _peek(self):
        """Olha o próximo caractere sem avançar."""
        peek_pos = self.position + 1
        if peek_pos < len(self.source):
            return self.source[peek_pos]
        return None

    def _error(self, message):
        """Lança um erro léxico."""
        raise Exception(f"Erro léxico na linha {self.line}, coluna {self.column}: {message}")

    def _skip_whitespace(self):
        """Ignora espaços em branco."""
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.column = 0 # Reseta coluna para a nova linha
            self._advance()

    def _skip_comment(self):
        """Ignora comentários de linha (//)."""
        if self.current_char == '/' and self._peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self._advance()
            self._skip_whitespace() # Chamar para pular a quebra de linha do comentário

    def _number(self):
        """Processa números inteiros."""
        result = ''
        start_column = self.column
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self._advance()
        return Token(TokenType.NUMERO_INTEIRO, result, self.line, start_column)

    def _string(self):
        """Processa literais de string (entre aspas duplas)."""
        start_column = self.column
        self._advance() # Pula a aspa de abertura
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self._advance()
        if self.current_char != '"':
            self._error("String não terminada. Esperava-se '\"'.")
        self._advance() # Pula a aspa de fechamento
        return Token(TokenType.STRING, result, self.line, start_column)

    def _identifier_or_keyword(self):
        """Processa identificadores ou palavras-chave."""
        result = ''
        start_column = self.column
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self._advance()
        
        token_type = self.keywords.get(result.upper(), TokenType.IDENTIFICADOR)
        return Token(token_type, result, self.line, start_column)

    def tokenize(self):
        """Gera a lista de tokens a partir do código fonte."""
        while self.current_char is not None:
            self._skip_whitespace()
            self._skip_comment() # Tentar pular comentário após pular espaços

            if self.current_char is None:
                break # Sai se chegou ao fim após pular espaços/comentários

            current_col = self.column

            if self.current_char.isdigit():
                self.tokens.append(self._number())
                continue
            
            if self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self._identifier_or_keyword())
                continue

            # Operadores e Símbolos de um caractere
            if self.current_char == '+':
                self.tokens.append(Token(TokenType.OP_SOMA, '+', self.line, current_col))
                self._advance()
            elif self.current_char == '-':
                self.tokens.append(Token(TokenType.OP_SUB, '-', self.line, current_col))
                self._advance()
            elif self.current_char == '*':
                self.tokens.append(Token(TokenType.OP_MULT, '*', self.line, current_col))
                self._advance()
            elif self.current_char == '/':
                if self._peek() == '/': # É um comentário de linha, já tratado por _skip_comment
                    self._skip_comment()
                else: # É operador de divisão
                    self.tokens.append(Token(TokenType.OP_DIV, '/', self.line, current_col))
                    self._advance()
            elif self.current_char == '=':
                if self._peek() == '=': # ==
                    self.tokens.append(Token(TokenType.IGUAL, '==', self.line, current_col))
                    self._advance()
                    self._advance()
                else: # = (atribuição)
                    self.tokens.append(Token(TokenType.IGUAL, '=', self.line, current_col))
                    self._advance()
            elif self.current_char == '!':
                if self._peek() == '=': # !=
                    self.tokens.append(Token(TokenType.DIFERENTE, '!=', self.line, current_col))
                    self._advance()
                    self._advance()
                else:
                    self._error(f"Caractere inesperado: '{self.current_char}'")
            elif self.current_char == '<':
                if self._peek() == '=': # <=
                    self.tokens.append(Token(TokenType.MENOR_IGUAL, '<=', self.line, current_col))
                    self._advance()
                    self._advance()
                else: # <
                    self.tokens.append(Token(TokenType.MENOR, '<', self.line, current_col))
                    self._advance()
            elif self.current_char == '>':
                if self._peek() == '=': # >=
                    self.tokens.append(Token(TokenType.MAIOR_IGUAL, '>=', self.line, current_col))
                    self._advance()
                    self._advance()
                else: # >
                    self.tokens.append(Token(TokenType.MAIOR, '>', self.line, current_col))
                    self._advance()
            elif self.current_char == '(':
                self.tokens.append(Token(TokenType.PARENTESE_ESQ, '(', self.line, current_col))
                self._advance()
            elif self.current_char == ')':
                self.tokens.append(Token(TokenType.PARENTESE_DIR, ')', self.line, current_col))
                self._advance()
            elif self.current_char == '{':
                self.tokens.append(Token(TokenType.CHAVE_ESQ, '{', self.line, current_col))
                self._advance()
            elif self.current_char == '}':
                self.tokens.append(Token(TokenType.CHAVE_DIR, '}', self.line, current_col))
                self._advance()
            elif self.current_char == ';':
                self.tokens.append(Token(TokenType.PONTO_VIRGULA, ';', self.line, current_col))
                self._advance()
            elif self.current_char == ',':
                self.tokens.append(Token(TokenType.VIRGULA, ',', self.line, current_col))
                self._advance()
            elif self.current_char == '"':
                self.tokens.append(self._string())
            else:
                self._error(f"Caractere inesperado: '{self.current_char}'")
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens