from abc import ABC, abstractmethod

class Forma(ABC):

    @abstractmethod
    def area(self):
        ...

    @abstractmethod
    def perimetro(self):
        ...

class Triangulo(Forma):

    def __init__(self, base: int, altura: int):
        self._base = base
        self._altura = altura

    def area(self):
        return (self._base * self._altura) / 2

    def perimetro(self):
        return (self._base * 3)

    def __str__(self):
        return (f"O Triângulo tem uma área de {self.area()}cm² e um perimetro de {self.perimetro()}cm ")

class Retangulo(Forma):

    def __init__(self, base: int, altura: int):
        self._base = base
        self._altura = altura
        
    def area(self):
        return (self._base * self._altura)
        
    def perimetro(self):
        return (self._base * 2) + (self._altura * 2)

    def __str__(self):
        return (f"O Retângulo tem uma área de {self.area()}cm² e um perimetro de {self.perimetro()}cm ")

class Quadrado(Forma):

    def __init__(self, lado: int):
        self._lado = lado

    def area(self):
        return (self._lado ** 2)

    def perimetro(self):
        return (self._lado * 4)

    def __str__(self):
            return (f"O Quadrado tem uma área de {self.area()}cm² e um perimetro de {self.perimetro()}cm ")

t1 = Triangulo(6, 8)
print(t1)

r1 = Retangulo(10, 20)
print(r1)

q1 = Quadrado(10)
print(q1)