class Veículo:
    def __init__(self, veiculo: str):
        self._veiculo = veiculo

    def __str__(self) -> str:
        return self._veiculo
    
class Motorista:
    def __init__(self, nome: str):
        self._nome = nome

    def dirigir(self, veiculo: Veículo):
            return print(f"O {veiculo} é dirigidp pelo condutor(a) {self._nome}")


motorista1 = Motorista("Maria Helena")
veiculo1 = Veículo("Pálio")
motorista1.dirigir(veiculo1)