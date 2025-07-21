class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing # Ambiente pai para escopo aninhado (futuro)

    def define(self, name: str, value):
        """Define uma nova variável no ambiente atual."""
        if name in self.values:
            raise Exception(f"Erro: Variável '{name}' já declarada neste escopo.")
        self.values[name] = value

    def assign(self, name: str, value):
        """Atribui um valor a uma variável existente."""
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing: # Se tiver um ambiente pai, tenta atribuir lá
            self.enclosing.assign(name, value)
            return
        raise ValueError(f"Variável '{name}' não definida.") # Use ValueError ou Exception sem "Erro:"

    def get(self, name: str):
        """Obtém o valor de uma variável."""
        if name in self.values:
            return self.values[name]
        if self.enclosing: # Se não encontrou no ambiente atual, procura no pai
            return self.enclosing.get(name)
        raise ValueError(f"Variável '{name}' não definida.") # Use ValueError ou Exception sem "Erro:"
    
    def exists(self, name: str) -> bool:
        """Verifica se uma variável existe no escopo atual ou em escopos pais."""
        if name in self.values:
            return True
        if self.enclosing:
            return self.enclosing.exists(name)
        return False