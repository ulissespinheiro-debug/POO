class Time:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self._jogadores: list["Jogador"] = []   # agregação: Time → Jogador

    def contratar(self, jogador: "Jogador") -> None:
        # se o jogador já tem time, sai dele antes
        if jogador.time is not None:
            jogador.time._jogadores.remove(jogador)
        self._jogadores.append(jogador)
        jogador.time = self

    @property
    def jogadores(self) -> list["Jogador"]:
        return list(self._jogadores)

    def __str__(self) -> str:
        nomes = ", ".join(j.nome for j in self._jogadores) or "sem jogadores"
        return f"{self.nome}: {nomes}"


class Jogador:
    def __init__(self, nome: str, posicao: str) -> None:
        self.nome = nome
        self.posicao = posicao
        self.time: Time | None = None

    def trocar_de_time(self, novo_time: Time) -> None:
        novo_time.contratar(self)

    def __str__(self) -> str:
        time = self.time.nome if self.time else "sem time"
        return f"{self.nome} ({self.posicao}) - {time}"


flamengo = Time("Flamengo")
palmeiras = Time("Palmeiras")

marco = Jogador("Marco", "Atacante")

flamengo.contratar(marco)
print(marco)
print(flamengo)

marco.trocar_de_time(palmeiras)
print(marco)       
print(flamengo)     
print(palmeiras)