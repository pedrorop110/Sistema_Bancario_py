from banco import consultar_saldo as consultar_saldodb
from banco import consultar_historico as consultar_historicodb
from banco import criar_conta as criar_contadb
from banco import depositar as depositardb
from banco import sacar as sacardb


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

    try:
        criar_contadb(cpf, nome, idade, saldo)
    except Exception as erro:
        print(f"Não foi possível criar a conta: {erro}")
        return

    print(f"Conta criada para {nome}.")


def depositar():
    cpf = input("Digite seu CPF: ")

    conta = consultar_saldodb(cpf)
    if conta is None:
        print("Conta não encontrada.")
        return

    valor = ler_valor_positivo("Digite uma quantia para depositar: R$ ")
    linhas_atualizadas = depositardb(cpf, valor)

    if linhas_atualizadas == 0:
        print("Não foi possível concluir o depósito.")
        return

    print(f"R$ {valor:.2f} depositados com sucesso para {conta[0]}.")


def sacar():
    cpf = input("Digite seu CPF para sacar: ")

    conta = consultar_saldodb(cpf)
    if conta is None:
        print("Conta não encontrada.")
        return

    valor = ler_valor_positivo("Quanto deseja sacar? R$ ")
    if valor > conta[1]:
        print("Saldo insuficiente.")
        return

    linhas_atualizadas = sacardb(cpf, valor)
    if linhas_atualizadas == 0:
        print("Não foi possível concluir o saque. Verifique o saldo e tente novamente.")
        return

    print(f"R$ {valor:.2f} sacados com sucesso para {conta[0]}.")


def consultar_saldo():
    cpf = input("Digite o CPF: ")
    info = consultar_saldodb(cpf)

    if info is None:
        print("Conta não encontrada.")
    else:
        print(f"{info[0]} possui um saldo de R$ {info[1]:.2f}.")


def ver_historico():
    cpf = input("Digite o CPF para ver o histórico: ")

    conta = consultar_saldodb(cpf)
    if conta is None:
        print("Conta não encontrada.")
        return

    historico = consultar_historicodb(cpf)
    if not historico:
        print(f"Ainda não há movimentações para {conta[0]}.")
        return

    print(f"\nHistórico de {conta[0]}:")
    for operacao, valor, data_hora in historico:
        print(f"{data_hora} — {operacao}: R$ {valor:.2f}")


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


if __name__ == "__main__":
    main()
