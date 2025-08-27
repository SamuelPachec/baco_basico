from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import datetime

saldo = 0.0
limite = 500
extrato = []
clientes = [
    {"nome": "João da Silva", "Data de Nascimento": "01/01/1990", "CPF": "12345678900", "endereco": {"logradouro": "Rua A", "nro": 123, "bairro": "Centro", "cidade": "São Paulo", "estado": "SP"}},
]

# contas armazenam cliente + saldo/extrato
contas = [
    {"agencia": "0001", "conta": 1, "cliente": clientes[0], "saldo": Decimal("0.00"), "extrato": [], "numero_saques": 0},
]

LIMITE_SAQUES = 3
LIMITE_TRANSACAO = 100  # limite por conta (total de registros no extrato) — ajustar conforme necessidade
LIMITE_POR_SAQUE = Decimal("500.00")
DECIMAL_CTX = Decimal("0.01")

def format_cpf(cpf):
    """Retorna CPF formatado XXX.XXX.XXX-XX ou None se inválido."""
    digits = ''.join(ch for ch in str(cpf) if ch.isdigit())
    if len(digits) != 11:
        return None
    return f"{digits[0:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"

def validar_cliente(cpf):
    """Retorna o dicionário do cliente se CPF encontrado, caso contrário None.
       Recebe cpf com ou sem formatação."""
    digits = ''.join(ch for ch in str(cpf) if ch.isdigit())
    for cliente in clientes:
        if ''.join(ch for ch in cliente.get("CPF", "") if ch.isdigit()) == digits:
            return cliente
    return None

def criar_cliente_dict(nome, data_nascimento, cpf, endereco):
    return {
        "nome": nome.strip(),
        "Data de Nascimento": data_nascimento.strip(),
        "CPF": ''.join(ch for ch in str(cpf) if ch.isdigit()),
        "endereco": endereco
    }

def cadastrar_cliente_interativo():
    nome = input("Informe o nome do cliente: ").strip()
    if not nome:
        print("Nome obrigatório.")
        return None

    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()
    cpf_raw = input("Informe o CPF (somente números ou já formatado): ").strip()
    cpf_fmt = format_cpf(cpf_raw)
    if cpf_fmt is None:
        print("CPF inválido. Informe 11 dígitos.")
        return None
    if validar_cliente(cpf_raw):
        print("CPF já cadastrado.")
        return None

    logradouro = input("Informe o logradouro: ").strip()
    nro = input("Informe o número: ").strip()
    bairro = input("Informe o bairro: ").strip()
    cidade = input("Informe a cidade: ").strip()
    estado = input("Informe o estado (sigla): ").strip()

    endereco = {"logradouro": logradouro, "nro": nro, "bairro": bairro, "cidade": cidade, "estado": estado}
    cliente = criar_cliente_dict(nome, data_nascimento, cpf_raw, endereco)
    clientes.append(cliente)
    print(f"\nSeja bem-vindo {nome}!\n")
    return cliente

def get_accounts_by_cpf(cpf):
    """Retorna lista de contas associadas ao CPF (pode ser vazia)."""
    digits = ''.join(ch for ch in str(cpf) if ch.isdigit())
    resultado = []
    for conta in contas:
        c_cpf = ''.join(ch for ch in conta.get("cliente", {}).get("CPF", "") if ch.isdigit())
        if c_cpf == digits:
            resultado.append(conta)
    return resultado

def criar_conta(cliente):
    """
    Cria conta vinculada a um cliente (aceita dict cliente ou CPF string).
    Permite que um cliente tenha várias contas; impede criação se cliente não existir.
    """
    if isinstance(cliente, str):
        cliente_obj = validar_cliente(cliente)
        if cliente_obj is None:
            print("Cliente não encontrado. Crie o cliente antes de criar a conta.")
            return None
    elif isinstance(cliente, dict):
        cliente_obj = cliente
    else:
        print("Parâmetro 'cliente' inválido.")
        return None

    agencia = "0001"
    conta_num = max((c.get("conta", 0) for c in contas), default=0) + 1
    nova_conta = {
        "agencia": agencia,
        "conta": conta_num,
        "cliente": cliente_obj,
        "saldo": Decimal("0.00"),
        "extrato": [],
        "numero_saques": 0
    }
    contas.append(nova_conta)
    print(f"Conta criada com sucesso! Agência: {agencia}, Conta: {conta_num}")
    return nova_conta

def listar_clientes():
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for cliente in clientes:
        nome = cliente.get("nome", "N/A")
        cpf = cliente.get("CPF", "")
        cpf_fmt = format_cpf(cpf) or cpf or "N/A"
        print(f"Nome: {nome} / CPF: {cpf_fmt}")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        cli = conta.get("cliente", {})
        nome = cli.get("nome", "N/A")
        cpf_fmt = format_cpf(cli.get("CPF", "")) or "N/A"
        saldo = conta.get("saldo", Decimal("0.00"))
        print(f"Agência: {conta['agencia']} | Conta: {conta['conta']} | Titular: {nome} | CPF: {cpf_fmt} | Saldo: R$ {saldo:.2f}")

def validar_transacao_conta(conta):
    if conta is None:
        print("Conta inválida.")
        return False
    if len(conta.get("extrato", [])) >= LIMITE_TRANSACAO:
        print("Operação falhou! Limite de transações atingido para esta conta.")
        return False
    return True

def visualizar_data():
    return datetime.datetime.now().strftime("%d/%m/%Y")

def visualizar_hora():
    return datetime.datetime.now().strftime("%H:%M")

def to_decimal(valor_str):
    try:
        d = Decimal(str(valor_str)).quantize(DECIMAL_CTX, rounding=ROUND_HALF_UP)
        return d
    except (InvalidOperation, TypeError):
        return None

def depositar_conta(conta, valor):
    if not validar_transacao_conta(conta):
        return False
    valor_dec = to_decimal(valor)
    if valor_dec is None or valor_dec <= 0:
        print("Valor inválido para depósito.")
        return False
    conta["saldo"] = (conta["saldo"] + valor_dec).quantize(DECIMAL_CTX)
    conta["extrato"].append(f"Depósito: R$ {valor_dec:.2f} - {visualizar_data()} às {visualizar_hora()}")
    print(f"Depósito de R$ {valor_dec:.2f} realizado com sucesso!")
    return True

def depositar_conta_interativo(conta):
    valor_str = input("Informe o valor do depósito: ").strip()
    valor_dec = to_decimal(valor_str)
    if valor_dec is None:
        print("Valor inválido. Use apenas números.")
        return
    depositar_conta(conta, valor_dec)

def sacar_conta(conta, valor):
    if not validar_transacao_conta(conta):
        return False
    valor_dec = to_decimal(valor)
    if valor_dec is None or valor_dec <= 0:
        print("Valor inválido para saque.")
        return False
    if conta["numero_saques"] >= LIMITE_SAQUES:
        print("Número máximo de saques diários atingido.")
        return False
    if valor_dec > LIMITE_POR_SAQUE:
        print(f"Valor excede o limite por saque: R$ {LIMITE_POR_SAQUE:.2f}")
        return False
    if valor_dec > conta["saldo"]:
        print("Saldo insuficiente.")
        return False
    conta["saldo"] = (conta["saldo"] - valor_dec).quantize(DECIMAL_CTX)
    conta["extrato"].append(f"Saque: R$ {valor_dec:.2f} - {visualizar_data()} às {visualizar_hora()}")
    conta["numero_saques"] += 1
    print(f"Saque de R$ {valor_dec:.2f} realizado com sucesso!")
    return True

def sacar_conta_interativo(conta):
    valor_str = input("Informe o valor do saque: ").strip()
    valor_dec = to_decimal(valor_str)
    if valor_dec is None:
        print("Valor inválido. Use apenas números.")
        return
    sacar_conta(conta, valor_dec)

def visualizar_extrato_conta(conta):
    print("\n========== EXTRATO ==========")
    if not conta["extrato"]:
        print("Não foram realizadas movimentações.")
    else:
        for linha in conta["extrato"]:
            print(linha)
            print("------------------------------")
    print(f"Saldo: R$ {conta['saldo']:.2f}")
    print("==============================\n")

# ----- fluxos de menu -----
def menu_inicial():
    return """
========== Início ==========
[cu] Criar usuário
[lg] Login
[lc] Listar clientes
[la] Listar contas
[q] Sair
===========================
Escolha uma opção: """

def menu_conta():
    return """
========== Conta ==========
[ac] Acessar conta (por CPF)
[cn] Criar nova conta (após cadastro)
[vc] Voltar ao menu inicial
===========================
Escolha uma opção: """

def menu_operacoes():
    return """
========== MENU ==========
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Criar nova conta
[lc] Listar clientes
[lo] Listar contas
[q] Logout
===========================
Escolha uma opção: """

# Loop principal
def main():
    while True:
        op = input(menu_inicial()).strip().lower()
        if op == "cu":
            cliente = cadastrar_cliente_interativo()
            if cliente:
                criar_agora = input("Deseja criar conta para este cliente agora? (s/n): ").strip().lower()
                if criar_agora == "s":
                    criar_conta(cliente)
        elif op == "lg":
            cpf = input("Informe o seu CPF: ").strip()
            cliente = validar_cliente(cpf)
            if cliente:
                print(f"Bem-vindo de volta, {cliente['nome']}!")
                # encontrar contas do cliente (agora pode ter várias)
                contas_cliente = get_accounts_by_cpf(cpf)
                conta = None
                if not contas_cliente:
                    print("Nenhuma conta encontrada para este cliente.")
                    if input("Criar conta agora? (s/n): ").strip().lower() == "s":
                        conta = criar_conta(cliente)
                        if not conta:
                            continue
                    else:
                        continue
                else:
                    if len(contas_cliente) == 1:
                        conta = contas_cliente[0]
                        escolha = input(f"Acessar conta {conta['conta']} (Ag {conta['agencia']}) ou digite 'c' para criar nova? [Enter=acessar]: ").strip().lower()
                        if escolha == "c":
                            conta = criar_conta(cliente)
                            if not conta:
                                continue
                        else:
                            print(f"Acessando conta {conta['conta']} (Ag {conta['agencia']}).")
                    else:
                        print("Contas encontradas:")
                        for c in contas_cliente:
                            saldo = c.get("saldo", Decimal("0.00"))
                            print(f"- Conta: {c['conta']} | Agência: {c['agencia']} | Saldo: R$ {saldo:.2f}")
                        escolha = input("Digite o número da conta que deseja acessar ou 'c' para criar nova: ").strip().lower()
                        if escolha == "c":
                            conta = criar_conta(cliente)
                            if not conta:
                                continue
                        else:
                            try:
                                num = int(escolha)
                                conta = next((c for c in contas_cliente if c["conta"] == num), None)
                                if conta is None:
                                    print("Conta não localizada. Operação cancelada.")
                                    continue
                            except ValueError:
                                print("Entrada inválida. Operação cancelada.")
                                continue

                # entra no menu de operações para esta conta
                while True:
                    op2 = input(menu_operacoes()).strip().lower()
                    if op2 == "d":
                        depositar_conta_interativo(conta)
                    elif op2 == "s":
                        sacar_conta_interativo(conta)
                    elif op2 == "e":
                        visualizar_extrato_conta(conta)
                    elif op2 == "nc":
                        nova = criar_conta(cliente)
                        if nova:
                            trocar = input("Conta criada. Deseja acessar a nova conta agora? (s/n): ").strip().lower()
                            if trocar == "s":
                                conta = nova
                                print(f"Acessando conta {conta['conta']} (Ag {conta['agencia']}).")
                    elif op2 == "lc":
                        listar_clientes()
                    elif op2 == "lo":
                        listar_contas()
                    elif op2 == "q":
                        print("Logout. Voltando ao menu inicial.")
                        break
                    else:
                        print("Operação inválida.")
            else:
                print("Cliente não encontrado. Por favor, cadastre-se primeiro.")
        elif op == "lc":
            listar_clientes()
        elif op == "la":
            listar_contas()
        elif op == "q":
            print("Saindo... Obrigado por utilizar o sistema!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
