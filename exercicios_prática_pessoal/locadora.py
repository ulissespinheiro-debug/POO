"""
QUESTÃO 9 — Locadora de carros (três classes)

- Modele Carro(placa, modelo, diaria), Cliente(cpf, nome) e Locadora.
- Carro nasce disponível e sem cliente. diaria é @property (> 0).
- Cliente: CPF validado por @staticmethod cpf_valido (11 dígitos, aceitando
  pontos e traço: "123.456.789-00"). Guarde SÓ os dígitos. Inválido -> CpfInvalidoError.
- Locadora: cadastrar_carro, cadastrar_cliente, alugar(placa, cpf),
  devolver(placa, dias) -> float, carros_disponiveis().
- Regra: cada cliente só pode ter UM carro alugado por vez.
- Exceções com base ErroDeLocadora: CarroNaoEncontradoError, ClienteNaoEncontradoError,
  CarroIndisponivelError, CarroNaoAlugadoError (devolver carro que não estava alugado),
  ClienteComPendenciaError, CpfInvalidoError.
- Carros iguais: mesma placa. Clientes iguais: mesmo CPF.
"""


# ---------- EXCEÇÕES ----------
class ErroDeLocadora(Exception): ...
class CarroNaoEncontradoError(ErroDeLocadora): ...
class ClienteNaoEncontradoError(ErroDeLocadora): ...
class CarroIndisponivelError(ErroDeLocadora): ...
class CarroNaoAlugadoError(ErroDeLocadora): ...
class ClienteComPendenciaError(ErroDeLocadora): ...
class CpfInvalidoError(ErroDeLocadora): ...


# ---------- CLIENTE ----------
class Cliente:
    def __init__(self, cpf: str, nome: str) -> None:
        if not Cliente.cpf_valido(cpf):
            raise CpfInvalidoError(f"CPF '{cpf}' inválido")
        self.cpf = Cliente.so_digitos(cpf)
        self.nome = nome

    @staticmethod
    def so_digitos(cpf: str) -> str:
        return cpf.replace(".", "").replace("-", "")

    @staticmethod
    def cpf_valido(cpf: str) -> bool:
        digitos = Cliente.so_digitos(cpf)
        return len(digitos) == 11 and digitos.isdigit()

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Cliente):
            return NotImplemented
        return self.cpf == outro.cpf

    def __str__(self) -> str:
        return f"{self.nome} (CPF {self.cpf})"


# ---------- CARRO ----------
class Carro:
    def __init__(self, placa: str, modelo: str, diaria: float) -> None:
        self.placa = placa.upper()
        self.modelo = modelo
        self.diaria = diaria
        self.disponivel = True
        self.cliente: Cliente | None = None     # nasce definido, mesmo vazio

    @property
    def diaria(self) -> float:
        return self._diaria

    @diaria.setter
    def diaria(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Diária deve ser maior que zero")
        self._diaria = valor

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Carro):
            return NotImplemented
        return self.placa == outro.placa

    def __str__(self) -> str:
        situacao = "disponível" if self.disponivel else f"alugado para {self.cliente.nome}"
        return f"{self.placa} - {self.modelo} - R$ {self.diaria:.2f}/dia - {situacao}"


# ---------- LOCADORA ----------
class Locadora:
    def __init__(self) -> None:
        self._carros: list[Carro] = []
        self._clientes: list[Cliente] = []

    def cadastrar_carro(self, carro: Carro) -> None:
        self._carros.append(carro)

    def cadastrar_cliente(self, cliente: Cliente) -> None:
        self._clientes.append(cliente)

    def _buscar_carro(self, placa: str) -> Carro:
        for carro in self._carros:
            if carro.placa == placa.upper():
                return carro
        raise CarroNaoEncontradoError(f"Carro {placa.upper()} não existe")

    def _buscar_cliente(self, cpf: str) -> Cliente:
        cpf = Cliente.so_digitos(cpf)
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                return cliente
        raise ClienteNaoEncontradoError(f"Cliente com CPF {cpf} não cadastrado")

    def _tem_pendencia(self, cliente: Cliente) -> bool:
        # any(...) é True se PELO MENOS UM carro estiver com esse cliente
        return any(carro.cliente == cliente for carro in self._carros)

    def alugar(self, placa: str, cpf: str) -> None:
        carro = self._buscar_carro(placa)
        cliente = self._buscar_cliente(cpf)
        if not carro.disponivel:
            raise CarroIndisponivelError(f"{carro.placa} já está alugado")
        if self._tem_pendencia(cliente):
            raise ClienteComPendenciaError(f"{cliente.nome} já tem um carro alugado")
        carro.disponivel = False
        carro.cliente = cliente

    def devolver(self, placa: str, dias: int) -> float:
        if dias < 1:
            raise ValueError("O aluguel deve ter pelo menos 1 dia")
        carro = self._buscar_carro(placa)
        if carro.disponivel:
            raise CarroNaoAlugadoError(f"{carro.placa} não estava alugado")
        valor = dias * carro.diaria
        carro.disponivel = True
        carro.cliente = None
        return valor

    def carros(self) -> list[Carro]:
        return list(self._carros)

    def carros_disponiveis(self) -> list[Carro]:
        return [c for c in self._carros if c.disponivel]


# ---------- PROGRAMA PRINCIPAL ----------
locadora = Locadora()
locadora.cadastrar_carro(Carro("abc1d23", "Gol", 120))
locadora.cadastrar_carro(Carro("XYZ9K87", "Onix", 150))
locadora.cadastrar_cliente(Cliente("123.456.789-00", "Ana"))
locadora.cadastrar_cliente(Cliente("98765432100", "Bruno"))

print("=== Sucesso ===")
locadora.alugar("ABC1D23", "12345678900")      # CPF sem pontos também acha
for carro in locadora.carros():
    print(carro)
print(f"Disponíveis: {len(locadora.carros_disponiveis())}")
print(f"Devolução do Gol: R$ {locadora.devolver('abc1d23', 4):.2f}")

print("\n=== Erros (capturados pela base) ===")
locadora.alugar("XYZ9K87", "123.456.789-00")   # Ana pega o Onix
tentativas = [
    ("Bruno pega o Onix alugado", lambda: locadora.alugar("XYZ9K87", "98765432100")),
    ("Ana pega um segundo carro", lambda: locadora.alugar("ABC1D23", "123.456.789-00")),
    ("Carro inexistente", lambda: locadora.alugar("ZZZ0Z00", "98765432100")),
    ("Cliente inexistente", lambda: locadora.alugar("ABC1D23", "111.111.111-11")),
    ("Devolver carro livre", lambda: locadora.devolver("ABC1D23", 2)),
    ("CPF inválido", lambda: Cliente("123", "Carla")),
]
# lambda = "função de uma linha guardada para rodar depois"
for descricao, acao in tentativas:
    try:
        acao()
    except ErroDeLocadora as erro:
        print(f"{descricao} -> {type(erro).__name__}: {erro}")