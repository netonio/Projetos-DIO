from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod
from datetime import datetime
import textwrap

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            print("Valor sacado com sucesso!")
            return True
        else:
            print("Operação inválida! Saldo insuficiente.")
            return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Valor depositado com sucesso!")
            return True
        else:
            print("Operação inválida! Digite um valor válido.")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor): 
        saques_realizados = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        if valor <= self.limite and saques_realizados < self.limite_saques:
            return super().sacar(valor)
        else:
            if valor >= self.limite:
                print("Operação inválida! Limite de valor de saque excedido")
            else:
                print("Operação inválida! Número de saques diários excedido")
        return False
    
    def __str__(self):
        return f"""
Agência: {self._agencia}
C/C: {self._numero}
Titular: {self.cliente._nome}
"""
    
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf,  endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor    

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao._valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente_por_cpf(cpf, clientes)

    if cliente:
        print("Operação inválida! Cliente com este CPF já existe,")
        return
    
    nome = input("Digite o nome completo do usuário: ")
    data_nascimento = input("Digite a  data de nascimento do usuário (dd/mm/aaaa): ").strip()
    endereco = input("Digite o endereço do usuário (logradouro, numero - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)

    clientes.append(cliente)

    print("Cliente cadastrado com sucesso!")
    
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("Operação inválida! Nenhum cliente encontrado.")

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")
    
def listar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("Operação inválida! Nenhum cliente encontrado.")
        return
    
    numero = int(input("Informe o número da conta: "))
    conta = recuperar_conta_cliente(numero, cliente)

    if not conta:
        print("Operação inválida! Nenhuma conta encontrada.")
        return

    print("==========Extrato==========")
    transacoes = conta.historico.transacoes
    if transacoes:
        for transacao in transacoes:
            if transacao["tipo"] == "Saque":
                print(f"{transacao['tipo'].ljust(20, '.')} -R${transacao['valor']:.2f}")
            else:
                print(f"{transacao['tipo'].ljust(20, '.')} +R${transacao['valor']:.2f}")
    else:
        print("Nenhuma operação econtrada!")

    s = "Saldo Atual:"
    print(f"{s.ljust(20, ".")} R${conta._saldo:.2f}")
    print("===========================")

def depositar_ou_sacar(operacao, clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    numero_conta = int(input("Informe o número da conta: "))
    conta = recuperar_conta_cliente(numero_conta, cliente)
    if not conta:
        print("Operação inválida! Nenhuma conta encontrada.")
        return
    
    valor = float(input(f"Informe o valor do {operacao.__name__.lower()}: "))
    if operacao.__name__ == "Saque":
        transacao = Saque(valor)
    else:
        transacao = Deposito(valor)
    
    cliente.realizar_transacao(conta, transacao)

def filtrar_cliente_por_cpf(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(numero_conta, cliente):
    if not cliente.contas:
        print("Operação inválida! Cliente não possui conta.")
        return
    
    contas_filtradas = [conta for conta in cliente.contas if conta._numero == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None

def main():
    menu = '''
----------MENU----------
        
[1] - Extrato
[2] - Sacar
[3] - Depositar
[4] - Cadastrar Usuário
[5] - Criar Conta Corrente
[6] - Listar Contas
[0] - Sair
                    
Digite o número correspondente a operação que deseja realizar: '''

    clientes = []
    contas = []

    while True:
        operacao = int(input(menu))

        if operacao == 1:
            exibir_extrato(clientes)

        elif operacao == 2:
            depositar_ou_sacar(Saque, clientes)

        elif operacao == 3:
            depositar_ou_sacar(Deposito, clientes)
            
        elif operacao == 4:
            criar_cliente(clientes)
        
        elif operacao == 5:
            numero_contas = len(contas) + 1
            criar_conta(numero_contas, clientes, contas)

        elif operacao == 6:
            listar_contas(contas)

        elif operacao == 0:
            break
        
        else:
            print("Operação inválida, verifique o número e tente novamente.")

main()