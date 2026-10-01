from __future__ import annotations

from decimal import Decimal, InvalidOperation
from enum import Enum


class MotivoErro(Enum):
    VALOR_INVALIDO = "valor_invalido"
    SALDO_INSUFICIENTE = "saldo_insuficiente"
    LIMITE_DE_SAQUE = "limite_de_saque"


class ErroDeConta(Exception):
    def __init__(self, motivo: MotivoErro, mensagem: str) -> None:
        super().__init__(mensagem)
        self.motivo: MotivoErro = motivo


def formatar(valor: Decimal) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Conta:
    LIMITE_SAQUE: Decimal = Decimal("5000.00")

    def __init__(self, saldo_inicial: Decimal = Decimal("0.00")) -> None:
        self._saldo: Decimal = saldo_inicial

    @property
    def saldo(self) -> Decimal:
        return self._saldo

    def depositar(self, valor: Decimal) -> None:
        self._validar_valor(valor)
        self._saldo += valor

    def sacar(self, valor: Decimal) -> None:
        self._validar_valor(valor)
        if valor > self.LIMITE_SAQUE:
            raise ErroDeConta(
                MotivoErro.LIMITE_DE_SAQUE,
                f"Limite por saque excedido: limite {formatar(self.LIMITE_SAQUE)}, "
                f"solicitado {formatar(valor)}.",
            )
        if valor > self._saldo:
            raise ErroDeConta(
                MotivoErro.SALDO_INSUFICIENTE,
                f"Saldo insuficiente: saldo {formatar(self._saldo)}, "
                f"saque solicitado {formatar(valor)}.",
            )
        self._saldo -= valor

    @staticmethod
    def _validar_valor(valor: Decimal) -> None:
        if valor <= 0:
            raise ErroDeConta(
                MotivoErro.VALOR_INVALIDO,
                f"Valor inválido: {valor}. Informe um valor maior que zero.",
            )


def ler_texto(prompt: str) -> str | None:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def ler_valor(prompt: str) -> Decimal | None:
    entrada = ler_texto(prompt)
    if entrada is None:
        return None
    try:
        valor = Decimal(entrada.replace(",", "."))
    except (InvalidOperation, ValueError):
        print("Entrada inválida: digite um número, por exemplo 150,50.")
        return None
    if not valor.is_finite():
        print("Entrada inválida: digite um número finito.")
        return None
    return valor.quantize(Decimal("0.01"))


def exibir_menu() -> None:
    print("\n=== Caixa Eletrônico ===")
    print("1 - Depositar")
    print("2 - Sacar")
    print("3 - Saldo")
    print("4 - Sair")


def executar_opcao(conta: Conta, opcao: str) -> bool:
    if opcao == "1":
        valor = ler_valor("Valor do depósito: ")
        if valor is not None:
            conta.depositar(valor)
            print(f"Depósito realizado. Saldo atual: {formatar(conta.saldo)}")
    elif opcao == "2":
        valor = ler_valor("Valor do saque: ")
        if valor is not None:
            conta.sacar(valor)
            print(f"Saque realizado. Saldo atual: {formatar(conta.saldo)}")
    elif opcao == "3":
        print(f"Saldo atual: {formatar(conta.saldo)}")
    elif opcao == "4":
        print("Encerrando. Até logo!")
        return False
    else:
        print("Opção inválida. Escolha entre 1 e 4.")
    return True


def main() -> None:
    conta = Conta()
    executando = True
    while executando:
        exibir_menu()
        opcao = ler_texto("Escolha uma opção: ")
        if opcao is None:
            print("Entrada encerrada. Saindo.")
            break
        try:
            executando = executar_opcao(conta, opcao)
        except ErroDeConta as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()