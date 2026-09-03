#Exercício 1:
class carro:
    renavam = "00123456789"
    marca = "Fiat"
    modelo = "Cronos"
    anoDeFabr = 2019
    def carrinho(self):
        print(f"O carro {self.marca} {self.modelo}, fabricado em {self.anoDeFabr}, possui o RENAVAM {self.renavam}.")

car1 = carro()
car1.carrinho()

#Exercício 2
class cachorro:
    raca = "Doberman"
    peso = "60Kg"
    idade = 7
    nome = "Zeus"
    def auau(self):
        print(f"O cachorro {self.nome} da raça {self.raca} de idade {self.idade} tem {self.peso}")

dog1 = cachorro()
dog1.auau() 


