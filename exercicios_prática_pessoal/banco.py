# ---------- EXCEÇÕES ----------
class ErroBancario(Exception): ...
class ContaNaoEncontradaError(ErroBancario): ...
class SaldoInsuficienteError(ErroBancario): ...
class ValorInvalidoError(ErroBancario): ...


# ---------- CONTA: representa UMA conta ----------
class Conta:
    def __init__(self, numero: str, titular: str, saldo: float = 0.0) -> None:
        self.numero = numero
        self.titular = titular
        self.saldo = saldo                      # já passa pelo setter

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        if valor < 0:                           # < e não <=
            raise ValueError("Saldo não pode ser negativo!")
        self._saldo = valor

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Conta):
            return NotImplemented
        return self.numero == outro.numero      # regra do enunciado

    def __str__(self) -> str:
        return f"Conta {self.numero} - {self.titular} - R$ {self.saldo:.2f}"


# ---------- BANCO: guarda VÁRIAS contas ----------
class Banco:
    def __init__(self) -> None:
        self._contas: list[Conta] = []

    def abrir_conta(self, conta: Conta) -> None:
        self._contas.append(conta)

    def contas(self) -> list[Conta]:
        return list(self._contas)               # cópia, para ninguém mexer na original

    def _buscar(self, numero: str) -> Conta:
        for conta in self._contas:
            if conta.numero == numero:
                return conta
        raise ContaNaoEncontradaError(f"Conta {numero} não existe")

    @staticmethod
    def _validar_valor(valor: float) -> None:
        if valor <= 0:                          # aqui sim é <=: depositar 0 não faz sentido
            raise ValorInvalidoError(f"Valor inválido: {valor}")

    def depositar(self, numero: str, valor: float) -> None:
        self._validar_valor(valor)
        conta = self._buscar(numero)
        conta.saldo += valor

    def sacar(self, numero: str, valor: float) -> None:
        self._validar_valor(valor)
        conta = self._buscar(numero)
        if valor > conta.saldo:
            raise SaldoInsuficienteError(f"Saldo insuficiente na conta {numero}")
        conta.saldo -= valor

    def transferir(self, origem: str, destino: str, valor: float) -> None:
        self._buscar(destino)                   # confere o destino ANTES de tirar o dinheiro
        self.sacar(origem, valor)
        self.depositar(destino, valor)


# ---------- PROGRAMA PRINCIPAL ----------
banco = Banco()
banco.abrir_conta(Conta("001", "Ana", 100))
banco.abrir_conta(Conta("002", "Bruno"))

# Sucesso
banco.depositar("001", 50)
banco.transferir("001", "002", 30)
for conta in banco.contas():
    print(conta)

# Erro: saldo insuficiente
try:
    banco.sacar("002", 1000)
except SaldoInsuficienteError as erro:
    print(f"Operação negada: {erro}")

# Erro: conta inexistente
try:
    banco.depositar("999", 10)
except ContaNaoEncontradaError as erro:
    print(f"Operação negada: {erro}")

# Erro: valor inválido
try:
    banco.depositar("001", -20)
except ValorInvalidoError as erro:
    print(f"Operação negada: {erro}")

# Erro: conta criada com saldo negativo
try:
    Conta("003", "Carla", -10)
except ValueError as erro:
    print(f"Conta não criada: {erro}")

# Igualdade
print(Conta("001", "Ana") == Conta("001", "Outra Pessoa"))   # True: mesmo número