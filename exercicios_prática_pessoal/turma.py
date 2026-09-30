"""
EXERCÍCIO 3 — Turma e notas

- Modele Aluno(matricula, nome, nota) e Turma(codigo).
- nota é @property: só aceita de 0 a 10, senão NotaInvalidaError.
- @staticmethod matricula_valida(matricula) -> bool: exatamente 8 dígitos numéricos.
  O __init__ do Aluno usa esse método e levanta MatriculaInvalidaError se falhar.
- Turma: matricular(aluno), lancar_nota(matricula, nota), aprovados() (nota >= 6),
  media() e ranking() (maior nota primeiro, usando __lt__ + sorted).
- Exceções com base ErroDeTurma: AlunoJaMatriculadoError, AlunoNaoEncontradoError,
  NotaInvalidaError, MatriculaInvalidaError.
- __str__ e __repr__ em Aluno. Dois alunos são iguais se tiverem a mesma matrícula.
- Pegadinha: media() de turma vazia não pode dar ZeroDivisionError.
"""


# ---------- EXCEÇÕES ----------
class ErroDeTurma(Exception): ...
class AlunoJaMatriculadoError(ErroDeTurma): ...
class AlunoNaoEncontradoError(ErroDeTurma): ...
class NotaInvalidaError(ErroDeTurma): ...
class MatriculaInvalidaError(ErroDeTurma): ...


# ---------- ALUNO ----------
class Aluno:
    def __init__(self, matricula: str, nome: str, nota: float = 0.0) -> None:
        if not Aluno.matricula_valida(matricula):
            raise MatriculaInvalidaError(f"Matrícula '{matricula}' deve ter 8 dígitos")
        self.matricula = matricula
        self.nome = nome
        self.nota = nota                    # passa pelo setter

    @staticmethod
    def matricula_valida(matricula: str) -> bool:
        return len(matricula) == 8 and matricula.isdigit()

    @property
    def nota(self) -> float:
        return self._nota

    @nota.setter
    def nota(self, valor: float) -> None:
        if not 0 <= valor <= 10:
            raise NotaInvalidaError(f"Nota {valor} fora do intervalo de 0 a 10")
        self._nota = valor

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Aluno):
            return NotImplemented
        return self.matricula == outro.matricula

    def __lt__(self, outro: object) -> bool:
        if not isinstance(outro, Aluno):
            return NotImplemented
        return self.nota < outro.nota

    def __str__(self) -> str:
        return f"{self.nome} ({self.matricula}) - nota {self.nota:.1f}"

    def __repr__(self) -> str:
        return f"Aluno({self.matricula!r}, {self.nome!r}, {self.nota})"


# ---------- TURMA ----------
class Turma:
    def __init__(self, codigo: str) -> None:
        self.codigo = codigo
        self._alunos: list[Aluno] = []

    def matricular(self, aluno: Aluno) -> None:
        if aluno in self._alunos:            # usa o __eq__ (matrícula)
            raise AlunoJaMatriculadoError(f"Matrícula {aluno.matricula} já está na turma")
        self._alunos.append(aluno)

    def _buscar(self, matricula: str) -> Aluno:
        for aluno in self._alunos:
            if aluno.matricula == matricula:
                return aluno
        raise AlunoNaoEncontradoError(f"Nenhum aluno com matrícula {matricula}")

    def lancar_nota(self, matricula: str, nota: float) -> None:
        self._buscar(matricula).nota = nota  # o setter valida

    def aprovados(self) -> list[Aluno]:
        return [a for a in self._alunos if a.nota >= 6]

    def media(self) -> float:
        if not self._alunos:                 # turma vazia: evita divisão por zero
            return 0.0
        return sum(a.nota for a in self._alunos) / len(self._alunos)

    def ranking(self) -> list[Aluno]:
        return sorted(self._alunos, reverse=True)   # sorted usa o __lt__


# ---------- PROGRAMA PRINCIPAL ----------
turma = Turma("POO-2026")
print(f"Média da turma vazia: {turma.media():.2f}")

turma.matricular(Aluno("20260001", "Ana"))
turma.matricular(Aluno("20260002", "Bruno"))
turma.matricular(Aluno("20260003", "Carla"))

turma.lancar_nota("20260001", 8.5)
turma.lancar_nota("20260002", 5.0)
turma.lancar_nota("20260003", 9.5)

print("\n=== Ranking ===")
# enumerate numera os itens: (1, aluno), (2, aluno)...
for posicao, aluno in enumerate(turma.ranking(), start=1):
    print(f"{posicao}º {aluno}")
print(f"Média: {turma.media():.2f}")
print(f"Aprovados: {turma.aprovados()}")    # lista usa o __repr__

print("\n=== Erros ===")
try:
    turma.matricular(Aluno("20260001", "Ana de Novo"))
except AlunoJaMatriculadoError as erro:
    print(f"Matrícula negada: {erro}")

try:
    turma.lancar_nota("99999999", 7)
except AlunoNaoEncontradoError as erro:
    print(f"Nota não lançada: {erro}")

try:
    turma.lancar_nota("20260002", 11)
except NotaInvalidaError as erro:
    print(f"Nota não lançada: {erro}")

try:
    Aluno("123", "Diego")
except MatriculaInvalidaError as erro:
    print(f"Aluno não criado: {erro}")

# Capturando pela BASE: pega qualquer erro da turma
try:
    turma.lancar_nota("20260003", -1)
except ErroDeTurma as erro:
    print(f"Erro da turma ({type(erro).__name__}): {erro}")