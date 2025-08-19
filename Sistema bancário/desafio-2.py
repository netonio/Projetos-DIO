def cadastrar_usuario(usuarios, nome, data_nascimento, cpf, endereco):
    usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}

    for i in usuarios:
        if cpf == i["cpf"]:
            print("Operação inválida! Usuário já cadastrado.")
            return

    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    
    for chave, valor in usuario.items():
        if chave == usuario:
            print(usuario["nome"])
        else:
            print(f"{chave}: {valor}")

    return usuarios

def criar_conta_corrente(contas, numero_conta, cpf, usuarios, agencia="0001"):
    if usuarios:
        for i in usuarios:
            if cpf == i["cpf"]:
                usuario = i
                numero = f"{numero_conta:04d}"
                conta = {"usuario": usuario, "numero_conta": numero, "agencia": agencia}

                contas.append(conta)
                numero_conta += 1
                print("Conta criada com sucesso!")

                for chave, valor in conta.items():
                    print(f"{chave}: {valor}")

                return contas, numero_conta
        else:
            print("Operação inválida! Usuário não encontrado, verifque o CPF ou cadastre um novo usuário")
            return contas, numero_conta
    else:
        print("Operação inválida! Nenhum usuário existente, cadastre um novo usuário")
        return contas, numero_conta

def tirar_extrato( saldo, /, *, extrato):
    print("==========Extrato==========")
    if extrato:
        for item in extrato:
            print(item)
    else:
        print("nenhuma operação econtrada")

    s = "Saldo Atual"
    print(f"{s.ljust(20, ".")} R${saldo:.2f}")

def sacar(*, saldo, saque, limite_diario, limite_saque, extrato):
    if saque > saldo:
        print("Operação inválida! Saldo atual é insuficiente.")

        return
    elif saque > limite_saque:
        print("Operaçao inválida! Valor de saque ultrapassa o valor limite.")

        return
    elif limite_diario > 3:
        print("Operação inválida! Limite de saques diário alcançado.")

        return
    else:
        saldo -= saque
        s = "Saque"
        extrato.append(f"{s.ljust(20, ".")} -R${saque:.2f}")

        print("Valor sacado com sucesso!")
        limite_diario += 1

        return saldo, extrato, limite_diario

def depositar(saldo, deposito, extrato, /):
    saldo += deposito
    d = "Depósito"
    extrato.append(f"{d.ljust(20, ".")} +R${deposito:.2f}")

    print("Valor depositado com sucesso!")

    return saldo, extrato

def main():
    menu = '''
----------MENU----------
        
[1] - Extrato
[2] - Sacar
[3] - Depositar
[4] - Cadastrar Usuário
[5] - Criar Conta Corrente
[0] - Sair
                    
Digite o número correspondente a operação que deseja realizar: '''

    usuarios = []
    contas = []
    numero_conta = 1
    extrato = []
    saldo = 0
    limite_diario = 0
    limite_saque = 500

    while True:
        operacao = int(input(menu))

        if operacao == 1:
            tirar_extrato(saldo, extrato=extrato)

        elif operacao == 2:
            if limite_diario > 3:
                print("Limite de saques alcançado, tente novamente amanhã.")
            else: 
                saque = float(input("Digite o valor do saque: "))
                saldo, extrato, limite_diario = sacar(saldo=saldo, saque=saque, limite_diario=limite_diario, limite_saque=limite_saque, extrato=extrato)

        elif operacao == 3:
            deposito = float(input("Digite o valor a ser depositado: "))

            if deposito <= 0:
                print("Operação falhou: Valor inválido, digite um valor acima de 0")
            else:
                saldo, extrato = depositar(saldo, deposito, extrato)
            
        elif operacao == 4:
            nome = input("Digite o nome completo do usuário: ")
            data_nascimento = input("Digite a  data de nascimento do usuário (dd/mm/aaaa): ").strip()
            cpf = input("Digite o CPF do usuário (somente números): ").strip()
            endereco = input("Digite o endereço do usuário (logradouro, numero - bairro - cidade/sigla estado): ")

            usuarios = cadastrar_usuario(usuarios, nome, data_nascimento, cpf, endereco)
        
        elif operacao == 5:
            cpf = input("Digite o CPF do usuário (somente números): ").strip()

            contas, numero_conta = criar_conta_corrente(contas, numero_conta, cpf, usuarios, )

        elif operacao == 0:
            break
        
        else:
            print("Operação inválida, verifique o número e tente novamente.")

main()