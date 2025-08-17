# 🏦 Banco Básico Terminal

Um sistema bancário simples feito em Python, para praticar lógica de programação e manipulação de funções.

---

## ✨ Funcionalidades

- **Depósito**
  - Permite adicionar dinheiro à conta.
  - Validação para aceitar apenas valores positivos.
  - Atualiza o saldo e registra a operação no extrato.

- **Saque**
  - Permite retirar dinheiro da conta.
  - Valida valor positivo, limite de saque, saldo suficiente e número máximo de saques diários.
  - Atualiza o saldo, registra no extrato e contabiliza o número de saques.

- **Extrato**
  - Exibe todas as movimentações (depósitos e saques).
  - Mostra o saldo atual.
  - Informa se não houver movimentações.

- **Sair**
  - Encerra o programa de forma amigável.

---

## 🛡️ Validações

- Não aceita valores negativos ou zero para depósito/saque.
- Saques não podem exceder o limite ou o saldo disponível.
- Limite máximo de saques diários.

---

## 🚀 Como funciona?

1. O usuário escolhe uma opção no menu: depositar, sacar, ver extrato ou sair.
2. O sistema executa a operação escolhida, mostrando mensagens claras sobre sucesso ou falha.
3. Todas as movimentações são registradas no extrato para consulta posterior.

---
> **Ideal para quem está começando a programar e quer entender lógica de operações