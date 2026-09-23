from rich.traceback import install
install(show_locals=True)

class SaldoInsuficienteError(Exception):
    """
    Saque maior do que o saldo indisponível

    """

class ValorInvalidoError(Exception):
    """
    Valores inválidos no depósito

    """

class ContaBancaria:
    def __init__(self, id, nome, saldo):
        self.id = id
        self.nome = nome
        self.saldo = saldo

    def sacar(self, valor):
        if valor > self.saldo:
            raise SaldoInsuficienteError(
                f"==Saldo Indisponível!==\n"
                f"Saldo: {self.saldo:.2f}\n"
                f"pedido de saque: {valor:.2f}"
            )
        self.saldo -= valor

    def deposito(self, valor):
        if valor != int:
            raise ValorInvalidoError(
                f"==Que Djabo tu digitou?==\n"
                f"Valor digitado errado, diferente de inteiro\n"
            )
        self.saldo += valor

conta1 = ContaBancaria(id=123, nome="belly", saldo=3000)
conta1.deposito("casa")
conta1.sacar(2)
print(F"A conta {conta1.id} cujo o dono(a) {conta1.nome} tem um saldo de {conta1.saldo:.2f}")