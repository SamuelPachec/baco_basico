menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def depositar(saldo, extrato):
    while True:
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("---------------------------------------------------")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            return saldo, extrato
        else:
            print("Operação falhou! O valor informado é inválido. Tente novamente com um valor maior que zero.")

def sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUES):
    while True:
        valor = float(input("Informe o valor do saque: "))
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido. Tente novamente com um valor maior que zero.")
        elif valor > limite:
            print("Operação falhou! O valor do saque excede o limite permitido.")
        elif numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques diários atingido.")
        elif valor > saldo:
            print("Operação falhou! Saldo insuficiente.")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("---------------------------------------------------")
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            return saldo, extrato, numero_saques
        return saldo, extrato, numero_saques

while True:
    opcao = input(menu)

    if opcao == "d":
        saldo, extrato = depositar(saldo, extrato)

    elif opcao == "s":
        saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, limite, LIMITE_SAQUES)

    elif opcao == "e":
        print("\n========== EXTRATO ==========")
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("=============================")

    elif opcao == "q":
        print("Saindo... Obrigado por utilizar o sistema!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")