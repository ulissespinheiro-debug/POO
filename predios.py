class Apartamento:
    def __init__(self, numero: int, andar: int):
        self.numero = numero
        self.andar = andar

    def __str__(self):
        return f"Apto {self.numero} ({self.andar} º andar)"

class Predio:
    def __init__(self, nome: str, andares: int):
        self._nome = nome
        self._andares = andares
        self._apartamento: list[Apartamento] = [
            Apartamento(numero=andar * 100 + 1, andar=andar)
            for andar in range(1, andares + 1)
        ]

    def __str__(self):
        return (f"O prédio {self._nome} tem {self._andares} andares."
                f"e {len(self._apartamento)} apartamentos.")

predio = Predio("Vila das rosas", 10)
print(predio)