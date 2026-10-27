from banco import consultar_saldo as consultar_saldodb
from banco import consultar_historico as consultar_historicodb
from banco import criar_conta as criar_contadb
from banco import depositar as depositardb
from banco import sacar as sacardb
from banco import buscar_conta as BuscarContadb

class conta:
    def __init__(self, nome, idade, cpf, saldo):
        self.nome = nome
        self.idade = idade
        self.cpf = cpf
        self.saldo = saldo

    def Salvar(self):
        criar_contadb(self.cpf, self.nome, self.idade, self.saldo)

    def Depositar(self, valor):
        linhas = depositardb(self.cpf, valor)
        if linhas == 0:
            return False
        self.saldo += valor
        return True

    def Sacar(self, valor):
        if valor > self.saldo:
            return False

        linhas = sacardb(self.cpf, valor)
        if linhas == 0:
            return False

        self.saldo -= valor
        return True

    def MostrarSaldo(self):
        print(f"{self.nome} possui um saldo de R$ {self.saldo:.2f}")


def ler_valor_positivo(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
        except ValueError:
            print("Digite um número válido.")
            continue

        if valor <= 0:
            print("Digite um valor maior que zero.")
            continue

        return valor


def criar_conta():
    cpf = input("CPF: ")
    nome = input("Nome: ")

    try:
        idade = int(input("Idade: "))
        saldo = float(input("Saldo inicial: "))
    except ValueError:
        print("Idade e saldo precisam ser números válidos.")
        return

    NovaConta = conta(nome, idade, cpf, saldo)

    try:
        NovaConta.Salvar()
    except Exception as erro:
        print(f"Não foi possível criar a conta: {erro}")
        return

    print(f"Conta criada para {NovaConta.nome}.")


def depositar():
    cpf = input("Digite seu CPF: ")

    dados = BuscarContadb(cpf)
    if dados is None:
        print("Conta não encontrada.")
        return

    MinhaConta = conta(nome=dados[0], idade=dados[1], cpf=dados[2], saldo=dados[3])

    # Parte do depósito
    valor = ler_valor_positivo("Digite uma quantia para depositar: R$ ")

    if not MinhaConta.Depositar(valor):
        print("Não foi possivel concluir o depósito.")
        return

    print(f"R$ {valor:.2f} depositados com sucesso para {MinhaConta.nome}.")


def sacar():
    cpf = input("Digite seu CPF: ")

    # Procurar Conta
    dados = BuscarContadb(cpf)
    if dados is None:
        print("Conta não encontrada.")
        return

    MinhaConta = conta(nome=dados[0], idade=dados[1], cpf=dados[2], saldo=dados[3])

    # Parte do saque
    valor = ler_valor_positivo("Quanto deseja sacar? R$ ")

    if not MinhaConta.Sacar(valor):
        print("Não foi possivel concluir o saque.")
        return

    print(f"R$ {valor:.2f} sacados com sucesso para {MinhaConta.nome}.")


def consultar_saldo():
    cpf = input("Digite o CPF: ")

    # Procurar Conta
    dados = BuscarContadb(cpf)
    if dados is None:
        print("Conta não encontrada.")
        return

    MinhaConta = conta(nome=dados[0], idade=dados[1], cpf=dados[2], saldo=dados[3])
    MinhaConta.MostrarSaldo()


def ver_historico():
    cpf = input("Digite o CPF para ver o histórico: ")

    # Procurar Conta
    dados = BuscarContadb(cpf)
    if dados is None:
        print("Conta não encontrada.")
        return

    nome = dados[0]
    
    historico = consultar_historicodb(cpf)
    if not historico:
        print(f"Ainda não há movimentações para {nome}.")
        return

    print(f"\nHistórico de {nome}:")
    for operacao, valor, data_hora in historico:
        print(f"{operacao}: R$ {valor:.2f}")


def main():
    while True:
        print("\n===== BANCO =====")
        print("1 - Criar conta")
        print("2 - Depositar")
        print("3 - Sacar")
        print("4 - Consultar saldo")
        print("5 - Ver histórico")
        print("6 - Sair")
        escolha = input("\nEscolha: ")

        if escolha == "1":
            criar_conta()
        elif escolha == "2":
            depositar()
        elif escolha == "3":
            sacar()
        elif escolha == "4":
            consultar_saldo()
        elif escolha == "5":
            ver_historico()
        elif escolha == "6":
            print("O usuário saiu.")
            break
        else:
            print("Opção inválida.")


main()
