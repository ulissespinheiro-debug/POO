"""
QUESTÃO 6 — Hotel

- Modele Quarto(numero, tipo, diaria) e Hotel.
- Todo quarto nasce livre (ocupado = False) e sem hóspede (hospede = None).
- tipo só pode ser "simples", "duplo" ou "suite". Guarde as opções num
  ATRIBUTO DE CLASSE chamado TIPOS. Tipo inválido -> ValueError.
- diaria é @property: deve ser maior que zero.
- Hotel: cadastrar(quarto), check_in(numero, hospede),
  check_out(numero, dias) -> float (valor a pagar),
  quartos_livres(tipo=None) -> livres, do mais barato para o mais caro.
- Exceções com base ErroDeHotel: QuartoNaoEncontradoError, QuartoOcupadoError,
  QuartoLivreError (check-out de quarto que já está livre), QuartoDuplicadoError.
- Dois quartos são iguais se tiverem o mesmo número. __lt__ compara pela diária.
- Programa principal demonstrando sucesso e erro.
"""


# ---------- EXCEÇÕES ----------
class ErroDeHotel(Exception): ...
class QuartoNaoEncontradoError(ErroDeHotel): ...
class QuartoOcupadoError(ErroDeHotel): ...
class QuartoLivreError(ErroDeHotel): ...
class QuartoDuplicadoError(ErroDeHotel): ...


# ---------- QUARTO ----------
class Quarto:
    TIPOS = ("simples", "duplo", "suite")     # atributo de classe

    def __init__(self, numero: int, tipo: str, diaria: float) -> None:
        if tipo.lower() not in Quarto.TIPOS:
            raise ValueError(f"Tipo '{tipo}' inválido. Use: {', '.join(Quarto.TIPOS)}")
        self.numero = numero
        self.tipo = tipo.lower()
        self.diaria = diaria
        self.ocupado = False
        self.hospede: str | None = None       # nasce definido, mesmo vazio

    @property
    def diaria(self) -> float:
        return self._diaria

    @diaria.setter
    def diaria(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Diária deve ser maior que zero")
        self._diaria = valor

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Quarto):
            return NotImplemented
        return self.numero == outro.numero

    def __lt__(self, outro: object) -> bool:
        if not isinstance(outro, Quarto):
            return NotImplemented
        return self.diaria < outro.diaria

    def __str__(self) -> str:
        situacao = f"ocupado por {self.hospede}" if self.ocupado else "livre"
        return f"Quarto {self.numero} ({self.tipo}) - R$ {self.diaria:.2f}/dia - {situacao}"


# ---------- HOTEL ----------
class Hotel:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self._quartos: list[Quarto] = []

    def cadastrar(self, quarto: Quarto) -> None:
        if quarto in self._quartos:
            raise QuartoDuplicadoError(f"Quarto {quarto.numero} já cadastrado")
        self._quartos.append(quarto)

    def _buscar(self, numero: int) -> Quarto:
        for quarto in self._quartos:
            if quarto.numero == numero:
                return quarto
        raise QuartoNaoEncontradoError(f"Quarto {numero} não existe")

    def check_in(self, numero: int, hospede: str) -> None:
        quarto = self._buscar(numero)
        if quarto.ocupado:
            raise QuartoOcupadoError(f"Quarto {numero} já está com {quarto.hospede}")
        quarto.ocupado = True
        quarto.hospede = hospede

    def check_out(self, numero: int, dias: int) -> float:
        if dias < 1:
            raise ValueError("A estadia deve ter pelo menos 1 dia")
        quarto = self._buscar(numero)
        if not quarto.ocupado:
            raise QuartoLivreError(f"Quarto {numero} já está livre")
        valor = dias * quarto.diaria
        quarto.ocupado = False
        quarto.hospede = None
        return valor

    def quartos_livres(self, tipo: str | None = None) -> list[Quarto]:
        livres = [q for q in self._quartos if not q.ocupado]
        if tipo is not None:
            livres = [q for q in livres if q.tipo == tipo.lower()]
        return sorted(livres)                 # usa __lt__ (diária)


# ---------- PROGRAMA PRINCIPAL ----------
hotel = Hotel("Hotel Caruaru")
hotel.cadastrar(Quarto(101, "simples", 120))
hotel.cadastrar(Quarto(102, "duplo", 200))
hotel.cadastrar(Quarto(201, "SUITE", 350))
hotel.cadastrar(Quarto(103, "simples", 110))

print("=== Sucesso ===")
hotel.check_in(201, "Ana")
print("Livres (mais barato primeiro):")
for quarto in hotel.quartos_livres():
    print(f"  {quarto}")
print("Livres do tipo simples:")
for quarto in hotel.quartos_livres("simples"):
    print(f"  {quarto}")
valor = hotel.check_out(201, 3)
print(f"Check-out do 201: R$ {valor:.2f}")

print("\n=== Erros ===")
hotel.check_in(101, "Bruno")
try:
    hotel.check_in(101, "Carla")
except QuartoOcupadoError as erro:
    print(f"Check-in negado: {erro}")

try:
    hotel.check_out(102, 2)
except QuartoLivreError as erro:
    print(f"Check-out negado: {erro}")

try:
    hotel.check_in(999, "Diego")
except QuartoNaoEncontradoError as erro:
    print(f"Check-in negado: {erro}")

try:
    hotel.cadastrar(Quarto(102, "duplo", 180))
except QuartoDuplicadoError as erro:
    print(f"Cadastro negado: {erro}")

try:
    Quarto(301, "cobertura", 900)
except ValueError as erro:
    print(f"Quarto não criado: {erro}")