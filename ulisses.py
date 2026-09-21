# Lista de Exercicios 1 - Fundamentos
# Programacao Orientada a Objetos - Sistemas para Internet
# Prof. Higor Morais
# Aluno: Ulisses

from __future__ import annotations


# ---------------------------------------------------------------------------
# Questao 6 - Classe Aluno
# ---------------------------------------------------------------------------
class Aluno:

    MEDIA_APROVACAO: float = 6.0

    def __init__(self, nome: str, matricula: str) -> None:
        self.nome: str = nome
        self.matricula: str = matricula
        # a lista comeca vazia e e criada por instancia (nunca como atributo de classe)
        self.notas: list[float] = []

    def lancar_nota(self, valor: float) -> None:
        if not 0.0 <= valor <= 10.0:
            raise ValueError("A nota deve estar entre 0 e 10.")
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


# ---------------------------------------------------------------------------
# Questao 8 - Classe Retangulo
# ---------------------------------------------------------------------------
class Retangulo:

    def __init__(self, base: float, altura: float) -> None:
        if base <= 0 or altura <= 0:
            raise ValueError("Base e altura devem ser positivas.")
        self.base: float = base
        self.altura: float = altura

    def area(self) -> float:
        return self.base * self.altura

    def perimetro(self) -> float:
        return 2 * (self.base + self.altura)

    def __eq__(self, outro: object) -> bool:
        # dois retangulos sao iguais quando tem as mesmas dimensoes
        if not isinstance(outro, Retangulo):
            return NotImplemented
        return self.base == outro.base and self.altura == outro.altura

    def __hash__(self) -> int:
        # ao definir __eq__ o __hash__ padrao e removido; reescrevemos para
        # manter o objeto utilizavel em sets e dicionarios
        return hash((self.base, self.altura))

    def __str__(self) -> str:
        return f"Retângulo {self.base} x {self.altura}"


# ---------------------------------------------------------------------------
# Questao 9 - Classe Data
# ---------------------------------------------------------------------------
class Data:

    DIAS_POR_MES: tuple[int, ...] = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    def __init__(self, dia: int, mes: int, ano: int) -> None:
        if not 1 <= mes <= 12:
            raise ValueError("Mês inválido.")
        if not 1 <= dia <= Data.dias_no_mes(mes, ano):
            raise ValueError("Dia inválido para o mês informado.")
        self.dia: int = dia
        self.mes: int = mes
        self.ano: int = ano

    @classmethod
    def de_texto(cls, texto: str) -> "Data":
        # construtor alternativo a partir de uma string "dd/mm/aaaa"
        partes: list[str] = texto.strip().split("/")
        if len(partes) != 3:
            raise ValueError("Formato esperado: dd/mm/aaaa")
        dia, mes, ano = (int(parte) for parte in partes)
        # cls permite que subclasses de Data tambem usem este metodo
        return cls(dia, mes, ano)

    @staticmethod
    def bissexto(ano: int) -> bool:
        # regra gregoriana: divisivel por 4, exceto seculos nao divisiveis por 400
        return ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0)

    @staticmethod
    def dias_no_mes(mes: int, ano: int) -> int:
        # auxiliar usada na validacao do dia
        if mes == 2 and Data.bissexto(ano):
            return 29
        return Data.DIAS_POR_MES[mes - 1]

    def __str__(self) -> str:
        # :02d garante os zeros a esquerda -> 09/08/2026
        return f"{self.dia:02d}/{self.mes:02d}/{self.ano:04d}"


# ---------------------------------------------------------------------------
# Testes / demonstracao
# ---------------------------------------------------------------------------
def main() -> None:
    # --- Questao 7: criar 3 alunos, lancar notas e imprimir so os aprovados ---
    alunos: list[Aluno] = [
        Aluno("Ana", "20261234"),
        Aluno("Bruno", "20265678"),
        Aluno("Carla", "20269012"),
    ]

    notas_por_aluno: list[list[float]] = [
        [8.0, 7.0, 7.5],   # Ana   -> media 7.5
        [4.0, 5.5, 6.0],   # Bruno -> media 5.2 (reprovado)
        [6.0, 6.0, 9.0],   # Carla -> media 7.0
    ]

    for aluno, notas in zip(alunos, notas_por_aluno):
        for nota in notas:
            aluno.lancar_nota(nota)

    print("Alunos aprovados:")
    for aluno in alunos:
        if aluno.aprovado():
            print(f"  {aluno}")

    # --- Questao 8 ---
    print("\nRetângulos:")
    r1 = Retangulo(3.0, 4.0)
    r2 = Retangulo(3.0, 4.0)
    r3 = Retangulo(5.0, 2.0)
    print(f"  {r1} -> área {r1.area()}, perímetro {r1.perimetro()}")
    print(f"  r1 == r2? {r1 == r2}")
    print(f"  r1 == r3? {r1 == r3}")

    # --- Questao 9 ---
    print("\nDatas:")
    d1 = Data(9, 8, 2026)
    d2 = Data.de_texto("03/09/2026")
    print(f"  {d1}")
    print(f"  {d2}")
    print(f"  2024 é bissexto? {Data.bissexto(2024)}")
    print(f"  1900 é bissexto? {Data.bissexto(1900)}")
    print(f"  2000 é bissexto? {Data.bissexto(2000)}")


if __name__ == "__main__":
    main()