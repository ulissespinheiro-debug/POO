class ErroDeConta(Exception):
    pass

class SaldoInsuficienteError(ErroDeConta):
    """
    Saque maior do que o saldo indisponível

    """
    def __init__(self, saldo, valor):
        super().__init__(f"==Saldo Indisponível!==\n"
                        f"Saldo: {saldo:.2f}\n"
                        f"pedido de saque: {valor:.2f}")
    
        
class ValorInvalidoError(ErroDeConta):
    """
    Valores inválidos no depósito

    """
    def __init__(self, valor):
        super().__init__(f"==Que Djabo tu digitou?==\n"
                        f"O valor {valor} não é permitido para depósito, o Máx é 1000")

class ContaBancaria:
    def __init__(self, id, nome, saldo):
        self.id = id
        self.nome = nome
        self.saldo = saldo

    def sacar(self, valor):
        if valor > self.saldo:
            raise SaldoInsuficienteError(self.saldo, valor)
        self.saldo -= valor

    def deposito(self, valor):
        if valor > 1000 or valor <= 0:
            raise ValorInvalidoError(valor)
        self.saldo += valor

conta1 = ContaBancaria(id=123, nome="belly", saldo=3000)
try:
    conta1.deposito(1100)
except ErroDeConta as e:
    print(f"Erro tratado: {e}")


try:
    conta1.sacar(300)
except ErroDeConta as e:
    print(f"Erro tratado: {e}")
    
print(F"A conta {conta1.id} cujo o dono(a) {conta1.nome} tem um saldo de {conta1.saldo:.2f}")