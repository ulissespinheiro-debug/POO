"""
EXERCÍCIO 5 — Cinema

- Modele Sessao(filme, horario, sala, capacidade) e Cinema.
- horario é "HH:MM": @staticmethod horario_valido valida o formato;
  @classmethod de_texto("Duna;19:30;3;80") cria a sessão.
- Ingressos vendidos nascem em 0, ficam PRIVADOS (__vendidos) e são expostos
  por uma property SOMENTE LEITURA (sem setter): ingressos_vendidos.
- Sessao: vender(qtd), lugares_livres().
- Cinema: adicionar_sessao, comprar(filme, horario, qtd), sessoes_do_filme(filme),
  programacao() (ordenada por horário via __lt__).
- Exceções: ErroDeCinema -> SessaoNaoEncontradaError, IngressosEsgotadosError,
  HorarioInvalidoError, ConflitoDeSalaError (mesma sala e mesmo horário).
- Duas sessões são iguais se tiverem mesma sala e mesmo horário (use isso no conflito).
"""


# ---------- EXCEÇÕES ----------
class ErroDeCinema(Exception): ...
class SessaoNaoEncontradaError(ErroDeCinema): ...
class IngressosEsgotadosError(ErroDeCinema): ...
class HorarioInvalidoError(ErroDeCinema): ...
class ConflitoDeSalaError(ErroDeCinema): ...


# ---------- SESSÃO ----------
class Sessao:
    def __init__(self, filme: str, horario: str, sala: int, capacidade: int) -> None:
        if not Sessao.horario_valido(horario):
            raise HorarioInvalidoError(f"Horário inválido: '{horario}'")
        if capacidade <= 0:
            raise ValueError("Capacidade deve ser positiva")
        self.filme = filme
        self.horario = horario
        self.sala = sala
        self.capacidade = capacidade
        self.__vendidos = 0               # PRIVADO: vira _Sessao__vendidos por baixo

    @staticmethod
    def horario_valido(horario: str) -> bool:
        partes = horario.split(":")
        if len(partes) != 2:
            return False
        hora, minuto = partes
        if len(hora) != 2 or len(minuto) != 2:
            return False
        if not (hora.isdigit() and minuto.isdigit()):
            return False
        return 0 <= int(hora) <= 23 and 0 <= int(minuto) <= 59

    @classmethod
    def de_texto(cls, texto: str) -> "Sessao":
        filme, horario, sala, capacidade = texto.split(";")
        return cls(filme, horario, int(sala), int(capacidade))

    @property
    def ingressos_vendidos(self) -> int:  # só getter: ninguém altera de fora
        return self.__vendidos

    def lugares_livres(self) -> int:
        return self.capacidade - self.__vendidos

    def vender(self, qtd: int) -> None:
        if qtd <= 0:
            raise ValueError("Quantidade deve ser positiva")
        if qtd > self.lugares_livres():
            raise IngressosEsgotadosError(
                f"{self.filme} às {self.horario}: pediram {qtd}, restam {self.lugares_livres()}")
        self.__vendidos += qtd

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Sessao):
            return NotImplemented
        return self.sala == outro.sala and self.horario == outro.horario

    def __lt__(self, outro: object) -> bool:
        if not isinstance(outro, Sessao):
            return NotImplemented
        # "09:15" < "14:00" funciona com texto porque sempre tem 2 dígitos!
        return self.horario < outro.horario

    def __str__(self) -> str:
        return (f"{self.horario} | Sala {self.sala} | {self.filme} "
                f"| {self.lugares_livres()} lugares livres")


# ---------- CINEMA ----------
class Cinema:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self._sessoes: list[Sessao] = []

    def adicionar_sessao(self, sessao: Sessao) -> None:
        if sessao in self._sessoes:       # __eq__: mesma sala + mesmo horário
            raise ConflitoDeSalaError(f"Sala {sessao.sala} já tem sessão às {sessao.horario}")
        self._sessoes.append(sessao)

    def _buscar(self, filme: str, horario: str) -> Sessao:
        for sessao in self._sessoes:
            if sessao.filme.lower() == filme.lower() and sessao.horario == horario:
                return sessao
        raise SessaoNaoEncontradaError(f"Não há sessão de '{filme}' às {horario}")

    def comprar(self, filme: str, horario: str, qtd: int) -> None:
        self._buscar(filme, horario).vender(qtd)

    def sessoes_do_filme(self, filme: str) -> list[Sessao]:
        return sorted(s for s in self._sessoes if s.filme.lower() == filme.lower())

    def programacao(self) -> list[Sessao]:
        return sorted(self._sessoes)


# ---------- PROGRAMA PRINCIPAL ----------
cine = Cinema("Cine IFRN")
cine.adicionar_sessao(Sessao("Duna", "19:30", 1, 3))
cine.adicionar_sessao(Sessao.de_texto("Interestelar;14:00;2;50"))
cine.adicionar_sessao(Sessao.de_texto("Duna;09:15;2;50"))

print("=== Sucesso ===")
cine.comprar("Duna", "19:30", 2)
for sessao in cine.programacao():                  # já sai em ordem de horário
    print(sessao)

print("\nSessões de Duna:")
for sessao in cine.sessoes_do_filme("duna"):
    print(f"  {sessao}")

teste = Sessao("Teste", "10:00", 9, 10)
teste.vender(3)
print(f"\nIngressos vendidos na sessão teste: {teste.ingressos_vendidos}")
try:
    teste.ingressos_vendidos = 0                   # property sem setter
except AttributeError:
    print("Não dá para alterar ingressos_vendidos de fora: é somente leitura!")

print("\n=== Erros (todos capturados pela base ErroDeCinema) ===")
try:
    cine.comprar("Duna", "19:30", 5)
except ErroDeCinema as erro:
    print(f"{type(erro).__name__}: {erro}")

try:
    cine.comprar("Avatar", "20:00", 1)
except ErroDeCinema as erro:
    print(f"{type(erro).__name__}: {erro}")

try:
    cine.adicionar_sessao(Sessao("Outro Filme", "19:30", 1, 100))
except ErroDeCinema as erro:
    print(f"{type(erro).__name__}: {erro}")

try:
    Sessao.de_texto("Duna;25:00;3;80")
except ErroDeCinema as erro:
    print(f"{type(erro).__name__}: {erro}")