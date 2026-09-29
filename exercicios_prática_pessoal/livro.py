class Livro:
    total_livros = 0

    def __init__(self, titulo, autor, preco):
        self.__titulo = titulo
        self.__autor = autor
        self.__preco = preco
        Livro.total_livros += 1

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, valor):
        if valor <= 0:
            raise ValueError("O preço deve ser maior do que 0!")
        self.__preco = valor

    @classmethod
    def de_string(cls, texto):
        titulo, autor, preco = texto.split(";")
        return cls(titulo, autor, float(preco))

    @staticmethod
    def preco_valido(valor):
        if valor > 0:
            return True
        else:
            return False

    def __str__(self,):
        return f"O livro {self.__titulo} do autor {self.__autor} custa a bagatela de {self.__preco}"

    def __eq__(self, outro):
        if not isinstance(outro, Livro):
            return NotImplemented
        return self.__titulo == outro.__titulo and self.__autor == outro.__autor
        

livro1 = Livro(titulo="Noites Brancas", autor="Fiódor Dostowesky", preco=40)
livro2 = Livro.de_string("Vidas secas; Graciliano Ramos; 30")
print(livro1)
print(livro2)
print(livro1 == livro2)
print(Livro.total_livros)