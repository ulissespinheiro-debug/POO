from rich.traceback import install
install(show_locals=True)

class Aluno:

    MEDIA_APROVACAO: float = 6.0

    def __init__(self, nome: str, matricula: str) -> None:
        self.nome: str = nome
        self.matricula: str = matricula
        # a lista comeca vazia e e criada por instancia (nunca como atributo de classe)
        self.notas: list[float] = []

    def lancar_nota(self, valor: float) -> None:
        if not 0.0 <= valor <= 10.0:
            raise ValueError("A nota deve estar entre 0 e 10.") # tá aí o tratamento explicando
        self.notas.append(valor)

    def media(self) -> float:
        # evita divisao por zero quando ainda nao ha notas
        if not self.notas:
            return 0.0
        return sum(self.notas) / len(self.notas)

    def aprovado(self) -> bool:
        return self.media() >= Aluno.MEDIA_APROVACAO

    def __str__(self) -> str:
        # formato pedido: "Ana (20261234) - media 7.5"
        return f"{self.nome} ({self.matricula}) — média {self.media():.1f}"
