class Animal:
    def __init__(self, nome: str) -> None:
        self._nome = nome
        self._posicao = 0
    
    def mover_se(self) -> None:
        self._posicao += 1

class Gato(Animal):
    def mover_se(self) -> None: # sobrescrita
        print(f"{self._nome} caminhando...")
        self._posicao += 1

class Peixe(Animal):
    def mover_se(self) -> None:
        print(f"{self._nome} nadando...")
        self._posicao += 1

class Passaro(Animal):
    def mover_se(self) -> None:
        print(f"{self._nome} voando...")
        self._posicao += 1

class Cobra(Animal):
    def mover_se(self) -> None:
        print(f"{self._nome} rastejando...")
        self._posicao += 1

def mover_todos(animais: list[Animal]) -> None:
        for animal in animais:
            animal.mover_se() # polimorfismo!

zoologico = [Gato("Sirius"),
            Peixe("Nemo"),
            Passaro("Mordecai"),
            Cobra("Clarisse")]

mover_todos(zoologico)

