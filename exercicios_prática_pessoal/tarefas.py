"""
QUESTÃO 10 — Gerenciador de tarefas

- Modele Tarefa(titulo, prioridade) e GerenciadorDeTarefas.
- Cada tarefa recebe um id AUTOMÁTICO e sequencial (1, 2, 3...), controlado por
  um ATRIBUTO DE CLASSE. A tarefa nasce não concluída.
- titulo não pode ser vazio (ValueError). prioridade é @property de 1 (mais urgente)
  a 5; fora disso -> PrioridadeInvalidaError.
- @classmethod de_dict({"titulo": "...", "prioridade": 2}) cria a tarefa
  (prioridade padrão 3 se não vier no dicionário).
- Tarefa.concluir(): se já estiver concluída -> TarefaJaConcluidaError.
- Gerenciador: adicionar(tarefa), concluir(id), remover(id), pendentes() (ordenadas),
  concluidas(), progresso() -> percentual concluído (0 se não houver tarefas).
- __lt__: ordena por prioridade e, empatando, por título em ordem alfabética.
- Duas tarefas são iguais se tiverem o mesmo título (ignorando maiúsculas);
  adicionar tarefa repetida -> TarefaDuplicadaError.
- Exceções com base ErroDeTarefas.
"""


# ---------- EXCEÇÕES ----------
class ErroDeTarefas(Exception): ...
class TarefaNaoEncontradaError(ErroDeTarefas): ...
class TarefaJaConcluidaError(ErroDeTarefas): ...
class TarefaDuplicadaError(ErroDeTarefas): ...
class PrioridadeInvalidaError(ErroDeTarefas): ...


# ---------- TAREFA ----------
class Tarefa:
    _proximo_id = 1                        # atributo de classe: contador global

    def __init__(self, titulo: str, prioridade: int = 3) -> None:
        if not titulo.strip():
            raise ValueError("O título não pode ser vazio")
        self.titulo = titulo.strip()
        self.prioridade = prioridade       # valida ANTES de gastar um id
        self.concluida = False
        self.id = Tarefa._proximo_id
        Tarefa._proximo_id += 1

    @property
    def prioridade(self) -> int:
        return self._prioridade

    @prioridade.setter
    def prioridade(self, valor: int) -> None:
        if not 1 <= valor <= 5:
            raise PrioridadeInvalidaError(f"Prioridade {valor} inválida (use de 1 a 5)")
        self._prioridade = valor

    @classmethod
    def de_dict(cls, dados: dict) -> "Tarefa":
        return cls(dados["titulo"], dados.get("prioridade", 3))

    def concluir(self) -> None:
        if self.concluida:
            raise TarefaJaConcluidaError(f"Tarefa #{self.id} já foi concluída")
        self.concluida = True

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Tarefa):
            return NotImplemented
        return self.titulo.lower() == outro.titulo.lower()

    def __lt__(self, outro: object) -> bool:
        if not isinstance(outro, Tarefa):
            return NotImplemented
        # Tuplas se comparam item a item: primeiro prioridade, depois título
        return (self.prioridade, self.titulo.lower()) < (outro.prioridade, outro.titulo.lower())

    def __str__(self) -> str:
        marca = "x" if self.concluida else " "
        return f"[{marca}] #{self.id} {self.titulo} (prioridade {self.prioridade})"

    def __repr__(self) -> str:
        return f"Tarefa({self.titulo!r}, {self.prioridade})"


# ---------- GERENCIADOR ----------
class GerenciadorDeTarefas:
    def __init__(self) -> None:
        self._tarefas: list[Tarefa] = []

    def adicionar(self, tarefa: Tarefa) -> None:
        if tarefa in self._tarefas:
            raise TarefaDuplicadaError(f"Já existe a tarefa '{tarefa.titulo}'")
        self._tarefas.append(tarefa)

    def _buscar(self, id_tarefa: int) -> Tarefa:
        for tarefa in self._tarefas:
            if tarefa.id == id_tarefa:
                return tarefa
        raise TarefaNaoEncontradaError(f"Não existe tarefa #{id_tarefa}")

    def concluir(self, id_tarefa: int) -> None:
        self._buscar(id_tarefa).concluir()      # a regra mora na Tarefa

    def remover(self, id_tarefa: int) -> None:
        self._tarefas.remove(self._buscar(id_tarefa))

    def pendentes(self) -> list[Tarefa]:
        return sorted(t for t in self._tarefas if not t.concluida)

    def concluidas(self) -> list[Tarefa]:
        return [t for t in self._tarefas if t.concluida]

    def progresso(self) -> float:
        if not self._tarefas:
            return 0.0
        return len(self.concluidas()) / len(self._tarefas) * 100


# ---------- PROGRAMA PRINCIPAL ----------
ger = GerenciadorDeTarefas()
print(f"Progresso sem tarefas: {ger.progresso():.0f}%")

ger.adicionar(Tarefa("Estudar POO", 1))
ger.adicionar(Tarefa("Lavar a louça", 4))
ger.adicionar(Tarefa.de_dict({"titulo": "Revisar exceções", "prioridade": 1}))
ger.adicionar(Tarefa.de_dict({"titulo": "Assistir série"}))      # prioridade 3

print("\n=== Sucesso ===")
ger.concluir(2)
print("Pendentes (mais urgente primeiro, empate em ordem alfabética):")
for tarefa in ger.pendentes():
    print(f"  {tarefa}")
print(f"Concluídas: {ger.concluidas()}")
print(f"Progresso: {ger.progresso():.0f}%")
ger.remover(4)
print(f"Depois de remover a #4: {ger.progresso():.0f}% concluído")

print("\n=== Erros ===")
try:
    ger.concluir(2)
except TarefaJaConcluidaError as erro:
    print(f"Negado: {erro}")

try:
    ger.concluir(99)
except TarefaNaoEncontradaError as erro:
    print(f"Negado: {erro}")

try:
    ger.adicionar(Tarefa("ESTUDAR POO", 2))
except TarefaDuplicadaError as erro:
    print(f"Negado: {erro}")

try:
    Tarefa("Dormir", 9)
except PrioridadeInvalidaError as erro:
    print(f"Negado: {erro}")

try:
    Tarefa("   ")
except ValueError as erro:
    print(f"Negado: {erro}")