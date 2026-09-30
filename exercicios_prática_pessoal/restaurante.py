"""
QUESTÃO 8 — Pedido de restaurante (três classes)

- Modele ItemCardapio(nome, preco), ItemPedido(item, quantidade) e Pedido(mesa).
- preco é @property (> 0). quantidade de ItemPedido deve ser positiva. mesa deve ser positiva.
- Pedido tem ATRIBUTO DE CLASSE TAXA_SERVICO = 0.10 (10%).
- O pedido nasce aberto. O estado "fechado" é PRIVADO e exposto por property
  somente leitura.
- Pedido: adicionar(item, quantidade=1) (se o item já estiver no pedido, soma a quantidade),
  remover(nome), subtotal(), total() (subtotal + taxa), fechar() -> float (retorna o total).
- Exceções com base ErroDePedido: PedidoFechadoError (mexer em pedido fechado),
  ItemNaoEncontradoError, PedidoVazioError (fechar pedido sem itens).
- Dois itens do cardápio são iguais se tiverem o mesmo nome (ignorando maiúsculas).
- __str__ do Pedido mostra a "comanda" completa.
"""


# ---------- EXCEÇÕES ----------
class ErroDePedido(Exception): ...
class PedidoFechadoError(ErroDePedido): ...
class ItemNaoEncontradoError(ErroDePedido): ...
class PedidoVazioError(ErroDePedido): ...


# ---------- ITEM DO CARDÁPIO ----------
class ItemCardapio:
    def __init__(self, nome: str, preco: float) -> None:
        self.nome = nome
        self.preco = preco

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Preço deve ser maior que zero")
        self._preco = valor

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, ItemCardapio):
            return NotImplemented
        return self.nome.lower() == outro.nome.lower()

    def __str__(self) -> str:
        return f"{self.nome} - R$ {self.preco:.2f}"


# ---------- ITEM DO PEDIDO (item + quantidade) ----------
class ItemPedido:
    def __init__(self, item: ItemCardapio, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        self.item = item
        self.quantidade = quantidade

    def subtotal(self) -> float:
        return self.item.preco * self.quantidade

    def __str__(self) -> str:
        return f"{self.quantidade}x {self.item.nome} = R$ {self.subtotal():.2f}"


# ---------- PEDIDO ----------
class Pedido:
    TAXA_SERVICO = 0.10

    def __init__(self, mesa: int) -> None:
        if mesa <= 0:
            raise ValueError("Número da mesa deve ser positivo")
        self.mesa = mesa
        self._itens: list[ItemPedido] = []
        self.__fechado = False

    @property
    def fechado(self) -> bool:
        return self.__fechado

    def _verificar_aberto(self) -> None:          # método interno reaproveitado
        if self.__fechado:
            raise PedidoFechadoError(f"O pedido da mesa {self.mesa} já foi fechado")

    def adicionar(self, item: ItemCardapio, quantidade: int = 1) -> None:
        self._verificar_aberto()
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        for item_pedido in self._itens:
            if item_pedido.item == item:          # __eq__ do ItemCardapio
                item_pedido.quantidade += quantidade
                return
        self._itens.append(ItemPedido(item, quantidade))

    def remover(self, nome: str) -> None:
        self._verificar_aberto()
        for item_pedido in self._itens:
            if item_pedido.item.nome.lower() == nome.lower():
                self._itens.remove(item_pedido)
                return
        raise ItemNaoEncontradoError(f"'{nome}' não está no pedido da mesa {self.mesa}")

    def subtotal(self) -> float:
        return sum(ip.subtotal() for ip in self._itens)

    def total(self) -> float:
        return self.subtotal() * (1 + Pedido.TAXA_SERVICO)

    def fechar(self) -> float:
        self._verificar_aberto()
        if not self._itens:
            raise PedidoVazioError(f"O pedido da mesa {self.mesa} não tem itens")
        self.__fechado = True
        return self.total()

    def __str__(self) -> str:
        linhas = [f"--- Mesa {self.mesa} ---"]
        linhas += [f"  {ip}" for ip in self._itens]
        linhas.append(f"  Subtotal: R$ {self.subtotal():.2f}")
        linhas.append(f"  Taxa ({Pedido.TAXA_SERVICO:.0%}): "
                      f"R$ {self.subtotal() * Pedido.TAXA_SERVICO:.2f}")
        linhas.append(f"  TOTAL: R$ {self.total():.2f}")
        return "\n".join(linhas)


# ---------- PROGRAMA PRINCIPAL ----------
baiao = ItemCardapio("Baião de dois", 32.00)
suco = ItemCardapio("Suco de caju", 8.50)
cocada = ItemCardapio("Cocada", 6.00)

print("=== Sucesso ===")
pedido = Pedido(5)
pedido.adicionar(baiao)
pedido.adicionar(suco, 2)
pedido.adicionar(ItemCardapio("SUCO DE CAJU", 8.50))   # mesmo item: soma, vira 3
pedido.adicionar(cocada)
pedido.remover("cocada")
print(pedido)
print(f"Fechado? {pedido.fechado}")
print(f"Valor cobrado: R$ {pedido.fechar():.2f}")
print(f"Fechado? {pedido.fechado}")

print("\n=== Erros ===")
try:
    pedido.adicionar(cocada)
except PedidoFechadoError as erro:
    print(f"Não adicionado: {erro}")

outro = Pedido(7)
try:
    outro.fechar()
except PedidoVazioError as erro:
    print(f"Não fechado: {erro}")

try:
    outro.remover("Picanha")
except ItemNaoEncontradoError as erro:
    print(f"Não removido: {erro}")

try:
    ItemCardapio("Água", 0)
except ValueError as erro:
    print(f"Item não criado: {erro}")