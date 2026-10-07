class Produto:
    def __init__(self, nome: str, preco: float) -> None:
        self.nome = nome
        self.preco = preco

class ItemPedido:
    def __init__(self, produto: Produto, quantidade: int) -> None:
        self.produto = produto # agregação
        self.quantidade = quantidade
    
    @property
    def subtotal(self) -> float:
        return self.produto.preco * self.quantidade

    def __str__(self) -> str:
        return f"{self.quantidade}x {self.produto.nome} = R$ {self.subtotal:.2f}"

class Pedido:
    def __init__(self, cliente: "Cliente") -> None:
        self.cliente = cliente # associação
        self._itens: list[ItemPedido] = []
    
    def adicionar(self, produto: Produto, quantidade: int) -> None:
        item = ItemPedido(produto, quantidade)
        self._itens.append(ItemPedido(produto, quantidade)) # composição

    @property
    def total(self) -> float:
        return sum(i.subtotal for i in self._itens)
    
    def __str__(self) -> str:
        linhas = "\n".join(f"  - {i}" for i in self._itens)
        return (f"Pedido de {self.cliente.nome}:\n{linhas}\n"
                f"Total: R$ {self.total:.2f}")

class Cliente:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self._pedidos: list[Pedido] = []

    def fazer_pedido(self) -> Pedido:
        pedido = Pedido(self)
        self._pedidos.append(pedido)
        return pedido

    @property
    def pedidos(self) -> list[Pedido]:
        return list(self._pedidos)

cliente = Cliente("Maria")
notebook = Produto("Notebook", 3500.00)
mouse = Produto("Mouse", 80.00)

pedido = cliente.fazer_pedido()
pedido.adicionar(notebook, 1)
pedido.adicionar(mouse, 2)

print(pedido)
print(f"\nPedidos de {cliente.nome}: {len(cliente.pedidos)}")
print(pedido.cliente is cliente)