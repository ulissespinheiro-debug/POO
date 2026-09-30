"""
EXERCÍCIO 4 — Estacionamento

- Modele Veiculo(placa, modelo) e Estacionamento(capacidade).
- Atributo DE CLASSE total_de_entradas: conta as entradas de TODOS os estacionamentos.
- capacidade deve ser positiva (validar no __init__).
- Estacionamento: entrar(veiculo), sair(placa), vagas_livres(), esta_estacionado(placa) -> bool.
- Exceções: EstacionamentoLotadoError, VeiculoJaEstacionadoError, VeiculoNaoEncontradoError.
- Dois veículos são iguais se tiverem a mesma placa.
- Método interno _buscar(placa) reaproveitado por sair e esta_estacionado.
- Pegadinha: esta_estacionado retorna bool, então trata a exceção do _buscar internamente.
"""


# ---------- EXCEÇÕES ----------
class ErroDeEstacionamento(Exception): ...
class EstacionamentoLotadoError(ErroDeEstacionamento): ...
class VeiculoJaEstacionadoError(ErroDeEstacionamento): ...
class VeiculoNaoEncontradoError(ErroDeEstacionamento): ...


# ---------- VEÍCULO ----------
class Veiculo:
    def __init__(self, placa: str, modelo: str) -> None:
        self.placa = placa.upper()        # padroniza: "abc1d23" vira "ABC1D23"
        self.modelo = modelo

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Veiculo):
            return NotImplemented
        return self.placa == outro.placa

    def __str__(self) -> str:
        return f"{self.placa} ({self.modelo})"

    def __repr__(self) -> str:
        return f"Veiculo({self.placa!r}, {self.modelo!r})"


# ---------- ESTACIONAMENTO ----------
class Estacionamento:
    total_de_entradas = 0                 # atributo DE CLASSE (compartilhado)

    def __init__(self, nome: str, capacidade: int) -> None:
        if capacidade <= 0:
            raise ValueError("Capacidade deve ser positiva")
        self.nome = nome
        self.capacidade = capacidade
        self._veiculos: list[Veiculo] = []

    def vagas_livres(self) -> int:
        return self.capacidade - len(self._veiculos)

    def entrar(self, veiculo: Veiculo) -> None:
        if veiculo in self._veiculos:
            raise VeiculoJaEstacionadoError(f"{veiculo.placa} já está no {self.nome}")
        if self.vagas_livres() == 0:
            raise EstacionamentoLotadoError(f"{self.nome} lotado ({self.capacidade} vagas)")
        self._veiculos.append(veiculo)
        # ATENÇÃO: é Estacionamento.total_de_entradas, e NÃO self.total_de_entradas.
        # "self.total_de_entradas += 1" criaria um atributo só DESTE objeto!
        Estacionamento.total_de_entradas += 1

    def _buscar(self, placa: str) -> Veiculo:
        for veiculo in self._veiculos:
            if veiculo.placa == placa.upper():
                return veiculo
        raise VeiculoNaoEncontradoError(f"{placa.upper()} não está no {self.nome}")

    def sair(self, placa: str) -> Veiculo:
        veiculo = self._buscar(placa)
        self._veiculos.remove(veiculo)
        return veiculo

    def esta_estacionado(self, placa: str) -> bool:
        try:
            self._buscar(placa)
            return True
        except VeiculoNaoEncontradoError:
            return False


# ---------- PROGRAMA PRINCIPAL ----------
centro = Estacionamento("Centro", 2)
shopping = Estacionamento("Shopping", 10)

print("=== Sucesso ===")
centro.entrar(Veiculo("abc1d23", "Gol"))
centro.entrar(Veiculo("XYZ9K87", "Onix"))
shopping.entrar(Veiculo("QWE4R56", "HB20"))

print(f"Vagas livres no Centro: {centro.vagas_livres()}")
print(f"ABC1D23 está no Centro? {centro.esta_estacionado('ABC1D23')}")
print(f"Total de entradas (todos os estacionamentos): {Estacionamento.total_de_entradas}")

saiu = centro.sair("abc1d23")
print(f"Saiu: {saiu}")
print(f"ABC1D23 ainda está no Centro? {centro.esta_estacionado('ABC1D23')}")

print("\n=== Erros ===")
try:
    centro.entrar(Veiculo("xyz9k87", "Onix"))      # já está lá
except VeiculoJaEstacionadoError as erro:
    print(f"Entrada negada: {erro}")

centro.entrar(Veiculo("AAA1A11", "Uno"))           # agora o Centro enche
try:
    centro.entrar(Veiculo("BBB2B22", "Fox"))
except EstacionamentoLotadoError as erro:
    print(f"Entrada negada: {erro}")

try:
    centro.sair("NAO0A00")
except VeiculoNaoEncontradoError as erro:
    print(f"Saída negada: {erro}")

try:
    Estacionamento("Fantasma", 0)
except ValueError as erro:
    print(f"Estacionamento não criado: {erro}")