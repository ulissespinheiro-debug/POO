from rich.traceback import install
install(show_locals=True)

class EstacionamentoLotadoError(Exception):
    """
    Trata do erro qaundo o estacionamento está cheio.
    
    """

class Estacionamento:
    def __init__(self, vagas: int):
        self.vagas = vagas

    def entrar(self, carros):
        if carros > self.vagas:
            raise EstacionamentoLotadoError(
                f"O número de vagas já foi excedida!"
            )
        self.vagas -= carros
        return carros

estacio1 = Estacionamento(30)
print(f"Após entrarem {estacio1.entrar(31)} carros, sobraram {estacio1.vagas} vagas")
                