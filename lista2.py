class SalarioInvalidoError(Exception): pass
class EmailInvalidoError(Exception): pass

class Funcionario:
    salario_minimo = 1621.00
    def __init__(self, nome: str , salario: float) -> object:
        self.nome = nome
        self.salario = salario

    @property
    def salario(self) -> None:
        return self.__salario

    @salario.setter
    def salario(self, valor) -> int:
        if valor <= self.salario_minimo:
            raise SalarioInvalidoError("Salário Menor do que o Mínimo")
        self.__salario = valor

    def aumentar(self, percentual) -> None:
        if percentual < 0 or percentual >= 0.3:
            raise ValueError("A porcentagem do aumento Salarial deve ser maior que 0 e menor que 30%")
        self.__salario += self.__salario * percentual
        return f"Salário Alterado! Agora seu salário é {self.__salario}"

    def __str__(self):
        return f"O funcionário {self.nome} tem o salário de R${self.__salario}"

class Email:
    def __init__(self, endereco):
        self.endereco = endereco

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, nome_email):
        if "@" not in nome_email or "." not in nome_email:
            raise EmailInvalidoError("Erro: O Email está faltando o '@', o '.' ou ambos.")
        self.__endereco = nome_email

    def __str__(self):
        return f"Email: {self.endereco}"

funcionario1 = Funcionario("Ulisses", 2500.00)
funcionario_email = Email("ulisses.pinheiro@gmail.com")
funcionario1.aumentar(0.1)
print(funcionario1, "\n", funcionario_email)

try:
    funcionario2 = Funcionario("Belly", 1620.00)
except SalarioInvalidoError as erro:
    print(f"{erro}")

try:
    funcionario1.aumentar(0.4)
except ValueError as erro:
    print(f"{erro}")

try:
    funcionario2_email = Email("bellyzoka.cabelin.gmail.com")
except EmailInvalidoError as erro:
    print(f"{erro}")