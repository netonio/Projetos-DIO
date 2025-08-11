menu = '''
-----Menu-----
        
1 - Extrato
2 - Sacar
3 - Depositar
0 - Sair
                    
Digite o número correspondente a operação que deseja realizar: '''

extrato = []
saldo = 0
limite_saques = 0

while True:
    operacao = int(input(menu))

    if operacao == 1:
        print("==========Extrato==========")
        if extrato:
            for item in extrato:
                print(item)
        else:
            print("nenhuma operação econtrada")

        s = "Saldo Atual"
        print(f"{s.ljust(20, ".")} R${saldo:.2f}")

    elif operacao == 2:
        if limite_saques > 3:
            print("Limite de saques alcançado, tente novamente amanhã.")
        else: 
            saque = float(input("Digite o valor do saque: "))

            if saque > saldo:
                print("Operação falhou: Saldo insuficiente, tente um valor menor.")
                print(f"Saldo atual: {saldo}")
            elif saque > 500:
                print("Operação falhou: Valor de saque ultrapassou o limite de 500, tente um valor menor.")
            else:
                saldo -= saque
                s = "Saque"
                extrato.append(f"{s.ljust(20, ".")} -R${saque:.2f}")
                limite_saques = limite_saques + 1

                print("Valor sacado com suceso!")

    elif operacao == 3:
        deposito = float(input("Digite o valor a ser depositado: "))

        if deposito <= 0:
            print("Operação falhou: Valor inválido, digite um valor acima de 0")
        else:
            saldo += deposito
            d = "Depósito"
            extrato.append(f"{d.ljust(20, ".")} +R${deposito:.2f}")

            print("Valor depositado com sucesso!")
        
    elif operacao == 0:
        break
    
    else:
        print("Operação inválida, verifique o número e tente novamente.")