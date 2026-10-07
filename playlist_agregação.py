class Musicas:
    def __init__(self, nome, duracao):
        self._nome = nome
        self._duracao = duracao

    @property
    def duracao(self) -> int:
        return self._duracao

    def __str__(self):
        return f"{self._nome} - {self._duracao}"

class CaixaDeSom:
    def reproduzir(self, musica: Musicas) -> None:
        print(f"♪ Tocando: {musica}")

class Playlist:
    def __init__(self, nomePlaylist):
        self._nomePlaylist = nomePlaylist
        self._playlist: list[Musicas] = []

    def adicionar(self, musica: Musicas):
        self._playlist.append(musica)

    def remover(self, musica: Musicas):
        if musica in self._playlist:
            self._playlist.remove(musica)

    def duracao_total(self) -> int:
        return sum(m.duracao for m in self._playlist)

    def tocar(self, caixa_de_som: CaixaDeSom) -> None:
        for musica in self._playlist:
            caixa_de_som.reproduzir(musica)

    def __str__(self):
        return f"Listas das músicas da playlista {self._nomePlaylist}: {self._playlist}"


musica1 = Musicas("Mágica", 3.49)
print(musica1)

playlist1 = Playlist("As melhores da calcinha preta")
playlist1.adicionar("Faço chover")
playlist1.adicionar("Duas Paixões")
playlist1.adicionar("Mágica")
playlist1.remover("Mágica")
print(playlist1)
CaixaDeSom()