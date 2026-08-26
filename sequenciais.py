questoes = int(input("Qual questão você quer ver miseravi? "))
match questoes:
    case 1:
        print("==Média de 4 notas==")
        n1 = int(input("Nota 1 : "))
        n2 = int(input("Nota 2 : "))
        n3 = int(input("Nota 3 : "))
        n4 = int(input("Nota 4 : "))
        print(f"Suas notas foram: {n1}, {n2}, {n3} e {n4}")
        media = ((n1 + n2 + n3 + n4)/4)
        print(f"Sua média foi {media}")