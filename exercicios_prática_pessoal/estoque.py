"""
EXERCÍCIO 2 — Estoque de loja

- Modele Produto(nome, preco, quantidade) e Estoque.
- preco é @property: deve ser maior que zero. quantidade não pode ser negativa.
- @classmethod de_texto("Caneta;2.50;10") devolve um Produto.
- Estoque: adicionar(produto), vender(nome, qtd), repor(nome, qtd),
  em_falta() (quantidade 0) e valor_total() (soma de preço x quantidade).
- Exceções: ProdutoNaoEncontradoError, EstoqueInsuficienteError, ProdutoDuplicadoError.
- Dois produtos são iguais se tiverem o mesmo nome, ignorando maiúsculas/minúsculas.
- Programa principal cobrindo sucesso e erros.
"""


# ---------- EXCEÇÕES ----------
class ErroDeEstoque(Exception): ...
class ProdutoNaoEncontradoError(ErroDeEstoque): ...
class EstoqueInsuficienteError(ErroDeEstoque): ...
class ProdutoDuplicadoError(ErroDeEstoque): ...


# ---------- PRODUTO: UMA coisa ----------
class Produto:
    def __init__(self, nome: str, preco: float, quantidade: int = 0) -> None:
        self.nome = nome
        self.preco = preco              # passa pelo setter (valida)
        self.quantidade = quantidade    # passa pelo setter (valida)

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Preço deve ser maior que zero")
        self._preco = valor

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("Quantidade não pode ser negativa")
        self._quantidade = valor

    @classmethod
    def de_texto(cls, texto: str) -> "Produto":
        # "Caneta;2.50;10"  ->  ["Caneta", "2.50", "10"]
        nome, preco, quantidade = texto.split(";")
        return cls(nome.strip(), float(preco), int(quantidade))

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Produto):
            return NotImplemented
        return self.nome.lower() == outro.nome.lower()

    def __str__(self) -> str:
        return f"{self.nome} - R$ {self.preco:.2f} ({self.quantidade} un.)"

    def __repr__(self) -> str:
        return f"Produto({self.nome!r}, {self.preco}, {self.quantidade})"


# ---------- ESTOQUE: guarda VÁRIAS coisas ----------
class Estoque:
    def __init__(self) -> None:
        self._produtos: list[Produto] = []

    def adicionar(self, produto: Produto) -> None:
        # O operador "in" usa o __eq__ por baixo dos panos!
        if produto in self._produtos:
            raise ProdutoDuplicadoError(f"'{produto.nome}' já está cadastrado")
        self._produtos.append(produto)

    def _buscar(self, nome: str) -> Produto:
        for produto in self._produtos:
            if produto.nome.lower() == nome.lower():
                return produto
        raise ProdutoNaoEncontradoError(f"'{nome}' não existe no estoque")

    @staticmethod
    def _validar_quantidade(qtd: int) -> None:
        if qtd <= 0:
            raise ValueError("A quantidade deve ser positiva")

    def vender(self, nome: str, qtd: int) -> None:
        self._validar_quantidade(qtd)
        produto = self._buscar(nome)
        if qtd > produto.quantidade:
            raise EstoqueInsuficienteError(
                f"Pediram {qtd}, mas só há {produto.quantidade} de '{produto.nome}'")
        produto.quantidade -= qtd

    def repor(self, nome: str, qtd: int) -> None:
        self._validar_quantidade(qtd)
        self._buscar(nome).quantidade += qtd

    def em_falta(self) -> list[Produto]:
        return [p for p in self._produtos if p.quantidade == 0]

    def valor_total(self) -> float:
        return sum(p.preco * p.quantidade for p in self._produtos)

    def produtos(self) -> list[Produto]:
        return list(self._produtos)     # cópia, para ninguém mexer na lista interna


# ---------- PROGRAMA PRINCIPAL ----------
estoque = Estoque()
estoque.adicionar(Produto("Caderno", 15.90, 20))
estoque.adicionar(Produto.de_texto("Caneta;2.50;10"))   # usando a fábrica
estoque.adicionar(Produto("Borracha", 1.00, 3))

print("=== Sucesso ===")
estoque.vender("caneta", 4)          # funciona mesmo em minúsculo
estoque.vender("Borracha", 3)        # zera a borracha
estoque.repor("Caderno", 5)
for produto in estoque.produtos():
    print(produto)
print(f"Em falta: {estoque.em_falta()}")        # lista usa o __repr__
print(f"Valor total: R$ {estoque.valor_total():.2f}")

print("\n=== Erros ===")
try:
    estoque.vender("Caderno", 100)
except EstoqueInsuficienteError as erro:
    print(f"Venda negada: {erro}")

try:
    estoque.repor("Lápis", 10)
except ProdutoNaoEncontradoError as erro:
    print(f"Reposição negada: {erro}")

try:
    estoque.adicionar(Produto("CADERNO", 20.00, 1))    # mesmo nome, outra caixa
except ProdutoDuplicadoError as erro:
    print(f"Cadastro negado: {erro}")

try:
    Produto("Régua", -3.00, 5)
except ValueError as erro:
    print(f"Produto inválido: {erro}")