# RoboScript: Interpretador para Linguagem de Controle de Robôs

Este repositório contém o projeto final da disciplina de **Compiladores**. Ele implementa um **interpretador para RoboScript**, uma linguagem de domínio específico (DSL) projetada para controlar movimentos e interações básicas de robôs em um ambiente simulado.

---

## Integrante

| Nome                    | Matrícula                    | Turma                    |
| ----------------------- | ---------------------------- | ------------------------ |
| Carlos Eduardo de Sousa Paz | 222022064 | Turma 02 |

## Introdução

Este projeto implementa um interpretador para a linguagem **RoboScript**, uma DSL desenvolvida especificamente para simular o controle de robôs. O interpretador foi construído seguindo as fases fundamentais estudadas em sala de aula na disciplina de Compiladores, ministrada pelo professor Fábio Mendes.

* **Análise Léxica:** transforma o código-fonte em uma sequência de tokens.
* **Análise Sintática:** constrói uma Árvore Sintática Abstrata (AST) a partir dos tokens, verificando a gramática da linguagem.
* **Interpretação:** percorre a AST para executar as ações simuladas do robô e gerenciar o estado da aplicação.

**RoboScript** é uma linguagem imperativa, de sintaxe simples e intuitiva, que permite escrever sequências de comandos para movimentar um robô virtual, girar, pegar/soltar objetos e interagir via mensagens.

---

## Sintaxe e Semântica de RoboScript

A linguagem RoboScript suporta os seguintes elementos e estruturas.

### Comandos de Movimento

```text
MOVER FRENTE <passos>;    # Move o robô para frente N passos
MOVER TRAS <passos>;      # Move o robô para trás N passos
GIRAR ESQUERDA;           # Gira o robô 90 graus para a esquerda
GIRAR DIREITA;            # Gira o robô 90 graus para a direita
```

### Comandos de Ação

```text
PEGAR;                               # O robô tenta pegar um objeto no local atual
SOLTAR;                              # O robô solta o objeto que está segurando
IMPRIMIR "<mensagem_ou_expressao>";  # Imprime mensagem ou valor de expressão
```

### Variáveis

Tipos suportados: **inteiros** e **strings**.

```text
VAR <nome_variavel> = <valor>;   # Declara e inicializa variável
SET <nome_variavel> = <expr>;    # Atribui novo valor à variável existente
```

Variáveis de estado (somente leitura) disponíveis durante a execução:

* `robot_x`
* `robot_y`
* `robot_direction`
* `has_object`

### Expressões Aritméticas e Lógicas

Operadores aritméticos: `+`, `-`, `*`, `/` (divisão inteira).

Operadores de comparação: `==`, `!=`, `<`, `>`, `<=`, `>=`.

Uso de parênteses `()` para agrupamento e precedência.

O operador `+` também concatena strings se um dos operandos for string.

### Estruturas de Controle

#### Condicionais (`SE` / `SENAO`)

```robo
SE (<condicao>) ENTAO {
    // Comandos executados se a condição for verdadeira
} SENAO {
    // Comandos executados se a condição for falsa
}
```

#### Laços (`REPETIR`)

```robo
REPETIR <numero_vezes_ou_expressao> VEZES {
    // Comandos a serem repetidos
}
```

### Comentários

```robo
// Comentário de linha única
```

---

## Instalação

Siga as instruções abaixo para configurar e executar o projeto em seu ambiente de desenvolvimento. O projeto é desenvolvido em **Python 3.9+** e utiliza **pip** para gerenciamento de dependências.

### Pré-requisitos

* Python 3.9 ou superior.
* Git (para clonar o repositório).

### Passos para Instalação

#### 1. Clone o Repositório

Abra o terminal e clone o projeto do GitHub.

```bash
git clone https://github.com/fcte-compiladores/trabalho-final-trabalho-final-compiladores.git
cd trabalho-final-trabalho-final-compiladores
```

---

#### 2. Crie e Ative um Ambiente Virtual (Recomendado)

Isole as dependências do projeto para evitar conflitos com outras instalações Python.

Crie o ambiente:

```bash
python -m venv venv
```

**Windows (PowerShell ou CMD):**

```powershell
.\venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Se tudo deu certo, você verá `(venv)` no prompt do terminal.

---

#### 3. Instale as Dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

---

#### 4. Configure o Pytest (Obrigatório para Testes)

Garanta que o Pytest encontre corretamente os módulos do projeto. Na raiz do repositório, inclua, se necessario, um arquivo **`pytest.ini`** com o conteúdo:

```ini
[pytest]
pythonpath = .
```

---

## Como Usar

### Executando o Interpretador RoboScript

Para executar um arquivo RoboScript (`.robo`), utilize:

```bash
python main.py <caminho/para/seu/arquivo.robo>
```
ou

```bash
python3 main.py <caminho/para/seu/arquivo.robo>
```

**Exemplo:**

```bash
python main.py exemplos/hello_robot.robo
```

---

### Rodando os Testes Unitários

Para garantir a correção do interpretador, execute a suíte de testes unitários com **Pytest**. A partir da raiz do projeto (e com o ambiente virtual ativado):

```bash
pytest
```
---

## Exemplos

A pasta `exemplos/` contém diversos arquivos `.robo` que demonstram a sintaxe e as capacidades do interpretador, com diferentes níveis de complexidade:

* **`hello_robot.robo`** – Exemplo simples: imprime mensagem, realiza movimento e giro.
* **`quadrado.robo`** – Demonstra variáveis e laço `REPETIR` para "desenhar" um quadrado.
* **`espiral_recursiva.robo`** – Simula padrão de movimento em espiral usando loops aninhados e decremento de variáveis (padrão recursivo simulado).
* **`exploracao_grid.robo`** – Usa condicionais (`SE`/`SENAO`) e variáveis de estado (`robot_x`, `robot_y`) para explorar um grid e "detectar" item.
* **`busca_caminho_simples.robo`** – Lógica simplificada de busca de caminho: o robô tenta se mover em direção a um destino com comparações e movimentos iterativos.

Para executar qualquer exemplo:

```bash
python main.py exemplos/nome_do_arquivo.robo
```
---

## Escopo Entregue vs Não Entregue
* Entregue: Movimentação básica, variáveis escalares (int/string), condicionais, laços, impressão, estado do robô.
* Não Entregue: Funções/recursão real, arrays/estruturas compostas, múltiplos robôs, ambiente gráfico, análise semântica estática.

---

## Estrutura do Código

A estrutura do repositório segue uma organização modular para facilitar a compreensão, manutenção e testes.

```text
trabalho-final-compiladores/
├── src/                      # Código-fonte principal do interpretador
│   ├── __init__.py           # Marca 'src' como pacote Python
│   ├── lexer.py              # Analisador Léxico
│   ├── parser.py             # Analisador Sintático
│   ├── ast_nodes.py          # Classes dos nós da AST
│   ├── interpreter.py        # Interpretador (tree-walking)
│   └── environment.py        # Ambiente de execução e variáveis
├── exemplos/                 # Exemplos de código RoboScript
│   ├── hello_robot.robo
│   ├── quadrado.robo
│   ├── espiral_recursiva.robo
│   ├── exploracao_grid.robo
│   └── busca_caminho_simples.robo
├── tests/                    # Testes unitários
│   ├── test_lexer.py         # Testes para o analisador léxico
│   ├── test_parser.py        # Testes para o analisador sintático
│   └── test_interpreter.py   # Testes para o interpretador
├── main.py                   # Ponto de entrada principal
├── pytest.ini                # Configuração do Pytest
├── README.md                 # Este arquivo de documentação
└── requirements.txt          # Dependências do projeto
```

---

## Detalhamento das Fases de Compilação no Código

### Análise Léxica

**Arquivo:** `src/lexer.py`

* A classe `Lexer` lê o código-fonte caractere a caractere.
* Identifica palavras-chave (`MOVER`, `SE`, `VAR` etc.), operadores (`+`, `=`, ...), literais (`"Olá"`, `10`), e identificadores (`robot_x`, `minha_variavel`).
* Gera uma sequência de objetos `Token` (tipo, valor, posição de linha/coluna) — crucial para mensagens de erro úteis.
* Ignora espaços em branco e comentários de linha (`//`).

---

### Análise Sintática

**Arquivo:** `src/parser.py`

* A classe `Parser` recebe a lista de tokens produzidos pelo `Lexer`.
* Implementa um **Analisador Sintático Descendente Recursivo**.
* Consome tokens com base na gramática definida para RoboScript e constrói a **Árvore Sintática Abstrata (AST)**.
* As classes declaradas em `src/ast_nodes.py` representam diferentes tipos de nós: declarações, expressões, comandos, etc.
* Valida se a sequência de tokens forma construções gramaticalmente corretas; gera erros sintáticos informativos.

---

## Interpretação

**Arquivo:** `src/interpreter.py`

* A classe `Interpreter` recebe a AST produzida pelo `Parser`.
* Implementa o padrão **Visitor** para percorrer a AST recursivamente (*tree-walking interpreter*).
* Para cada tipo de nó, há um método `visit_<NomeDoNo>` correspondente.
* Realiza análise semântica dinâmica durante a travessia (por ex.: verificação de tipos em tempo de execução; prevenção de divisão por zero; resolução de variáveis).
* Simula as ações do robô (movimento, giro, pegar/soltar) exibindo resultados no console.
* Utiliza `src/environment.py` para gerenciar escopos e valores de variáveis durante a execução.

---

## Bugs/Limitações/Problemas Conhecidos

O interpretador RoboScript, apesar de funcional, possui as seguintes limitações principais:

* Comandos Robóticos Básicos: Suporta apenas movimentos e ações fundamentais, sem recursos avançados como sensores complexos, manipulação de múltiplos objetos ou comunicação entre robôs.

* Tipagem Simplificada: Utiliza tipagem dinâmica, sem verificação de tipos em tempo de "compilação", apenas em tempo de execução para certas operações.

* Ausência de Recursão Explícita: Não há suporte direto para chamadas recursivas.

* Simulação Abstrata: O ambiente e o robô são representados apenas por texto no console, sem interface gráfica ou física.

---

## Referências

Para o projeto foram utiliizadas as referências abaixo, que orientaram a construção do interpretador em suas diversas fases.

**VANINI, F. A. Construção de Compiladores: Parte 1: Introdução, linguagens e gramáticas. Campinas: IC - Unicamp**. Disponível em: https://www.ic.unicamp.br/~vanini/mc910/Parte1.pdf. Acesso em: 21 jul. 2025.

**TOMASETTI, Federico. Parsing in Python: all the tools and libraries you can use. Tomassetti.me**. Disponível em: https://tomassetti.me/parsing-in-python/. Acesso em: 21 jul. 2025.

**FARIA, Daniel; BAPTISTA, Tiago João; HENRIQUES, Pedro Rangel. Upgrade of Lark Compiler Generator to Support Attribute Grammars**. Disponível em: https://drops.dagstuhl.de/storage/01oasics/oasics-vol120-slate2024/OASIcs.SLATE.2024.7/OASIcs.SLATE.2024.7.pdf. Acesso em: 21 jul. 2025.

**SHINAN, Erez. Lark documentation**. Disponível em: https://lark-parser.readthedocs.io/en/stable/. Acesso em: 21 jul. 2025.

**PYTEST.ORG. pytest documentation**. Disponível em: https://docs.pytest.org/en/stable/. Acesso em: 21 jul. 2025.

**MENDES, Fábio. 2025-1, 2025**. Disponível em: https://github.com/fcte-compiladores/2025-1. Acesso em: 21 jul. 2025.


