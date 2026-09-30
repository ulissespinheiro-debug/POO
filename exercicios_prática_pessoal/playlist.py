"""
QUESTÃO 7 — Playlist de músicas

- Modele Musica(titulo, artista, duracao) e Playlist(nome).
- duracao fica em SEGUNDOS e é @property: deve ser maior que zero.
- @staticmethod para_segundos("4:35") -> 275 e @staticmethod formatar(275) -> "4:35".
- @classmethod de_texto("Evidências;Chitãozinho & Xororó;4:35") cria a música.
- Playlist: adicionar(musica), remover(titulo), duracao_total() -> "mm:ss",
  tocar_proxima() -> Musica (toca em ordem; depois da última, volta para a primeira).
- len(playlist) deve retornar a quantidade de músicas (dunder __len__).
- Exceções com base ErroDePlaylist: MusicaDuplicadaError, MusicaNaoEncontradaError,
  PlaylistVaziaError (tocar playlist vazia).
- Duas músicas são iguais se tiverem mesmo título e artista (ignorando maiúsculas).
- __str__ no formato "Título - Artista (4:35)" e __repr__.
"""


# ---------- EXCEÇÕES ----------
class ErroDePlaylist(Exception): ...
class MusicaDuplicadaError(ErroDePlaylist): ...
class MusicaNaoEncontradaError(ErroDePlaylist): ...
class PlaylistVaziaError(ErroDePlaylist): ...


# ---------- MÚSICA ----------
class Musica:
    def __init__(self, titulo: str, artista: str, duracao: int) -> None:
        self.titulo = titulo
        self.artista = artista
        self.duracao = duracao

    @property
    def duracao(self) -> int:
        return self._duracao

    @duracao.setter
    def duracao(self, segundos: int) -> None:
        if segundos <= 0:
            raise ValueError("Duração deve ser maior que zero")
        self._duracao = segundos

    @staticmethod
    def para_segundos(texto: str) -> int:
        minutos, segundos = texto.split(":")      # "4:35" -> "4", "35"
        return int(minutos) * 60 + int(segundos)

    @staticmethod
    def formatar(segundos: int) -> str:
        return f"{segundos // 60}:{segundos % 60:02d}"   # :02d -> "5" vira "05"

    @classmethod
    def de_texto(cls, texto: str) -> "Musica":
        titulo, artista, tempo = texto.split(";")
        return cls(titulo, artista, cls.para_segundos(tempo))

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Musica):
            return NotImplemented
        return (self.titulo.lower() == outro.titulo.lower()
                and self.artista.lower() == outro.artista.lower())

    def __str__(self) -> str:
        return f"{self.titulo} - {self.artista} ({Musica.formatar(self.duracao)})"

    def __repr__(self) -> str:
        return f"Musica({self.titulo!r}, {self.artista!r}, {self.duracao})"


# ---------- PLAYLIST ----------
class Playlist:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self._musicas: list[Musica] = []
        self._posicao = 0                 # qual música toca a seguir

    def adicionar(self, musica: Musica) -> None:
        if musica in self._musicas:
            raise MusicaDuplicadaError(f"'{musica.titulo}' já está na playlist")
        self._musicas.append(musica)

    def remover(self, titulo: str) -> None:
        for musica in self._musicas:
            if musica.titulo.lower() == titulo.lower():
                self._musicas.remove(musica)
                return                    # achou e removeu: sai do método
        raise MusicaNaoEncontradaError(f"'{titulo}' não está na playlist")

    def duracao_total(self) -> str:
        return Musica.formatar(sum(m.duracao for m in self._musicas))

    def tocar_proxima(self) -> Musica:
        if not self._musicas:
            raise PlaylistVaziaError(f"A playlist '{self.nome}' está vazia")
        # o % (resto da divisão) faz a posição "dar a volta" no fim da lista
        musica = self._musicas[self._posicao % len(self._musicas)]
        self._posicao = (self._posicao + 1) % len(self._musicas)
        return musica

    def __len__(self) -> int:
        return len(self._musicas)

    def __str__(self) -> str:
        return f"Playlist '{self.nome}' - {len(self)} músicas - {self.duracao_total()}"


# ---------- PROGRAMA PRINCIPAL ----------
playlist = Playlist("Estudar POO")
playlist.adicionar(Musica.de_texto("Evidências;Chitãozinho & Xororó;4:35"))
playlist.adicionar(Musica("Asa Branca", "Luiz Gonzaga", 185))
playlist.adicionar(Musica.de_texto("Anunciação;Alceu Valença;3:58"))

print("=== Sucesso ===")
print(playlist)
print(f"Quantidade (len): {len(playlist)}")
for _ in range(4):                        # 4 vezes com 3 músicas: volta pra primeira
    print(f"Tocando: {playlist.tocar_proxima()}")
playlist.remover("asa branca")
print(f"Depois de remover: {playlist}")

print("\n=== Erros ===")
try:
    playlist.adicionar(Musica("EVIDÊNCIAS", "chitãozinho & xororó", 275))
except MusicaDuplicadaError as erro:
    print(f"Não adicionada: {erro}")

try:
    playlist.remover("Garota de Ipanema")
except MusicaNaoEncontradaError as erro:
    print(f"Não removida: {erro}")

try:
    Playlist("Vazia").tocar_proxima()
except PlaylistVaziaError as erro:
    print(f"Não tocou: {erro}")

try:
    Musica("Silêncio", "Ninguém", 0)
except ValueError as erro:
    print(f"Música não criada: {erro}")