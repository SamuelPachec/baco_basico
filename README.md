# 🏦 Banco Básico Terminal

Versão melhorada do sistema bancário em Python (terminal). Suporta múltiplas contas por usuário, operações por conta e tratamento mais robusto de valores monetários.

---

## ✅ Principais melhorias implementadas

- Usuário pode ter mais de uma conta; cada conta pertence a exatamente um usuário (não existem contas sem usuário).
- Login por CPF (com ou sem formatação).
- Criação de conta disponível após cadastro ou no momento do login.
- Operações por conta: depositar, sacar e visualizar extrato.
- Uso de Decimal para valores monetários (precisão e arredondamento).
- Formatação/validação de CPF para o padrão `XXX.XXX.XXX-XX`.
- Controle de limites:
  - limite por saque (ex.: R$ 500,00)
  - limite diário de número de saques por conta
  - limite total de transações por conta (extrato)
- Extrato por conta (lista de movimentações com data/hora).
- Menus separados: menu inicial, menu de conta e menu de operações.
- Entradas validadas e mensagens de erro claras.
- Dados de exemplo (um cliente e uma conta) para teste.

---

## ⚙️ Requisitos

- Python 3.8+
- Módulos padrão: decimal, datetime (nenhuma dependência externa necessária)

---

## ▶️ Como executar

1. Abra terminal no diretório do projeto:
   c:\Users\samuel.alves\Pessoal\DIO(Suzano)\banco_basico
2. Execute:
   ```
   python app.py
   ```
3. Use o menu para criar usuário, fazer login, criar/selecionar contas e operar.

---

## 🧭 Fluxo de uso (resumido)

1. No menu inicial:
   - [cu] Criar usuário
   - [lg] Login (por CPF)
   - [lc] Listar clientes
   - [la] Listar contas
   - [q] Sair
2. Após login, se o usuário tiver contas:
   - Escolha a conta ou crie nova
3. No menu de operações da conta:
   - [d] Depositar
   - [s] Sacar
   - [e] Extrato
   - [nc] Criar nova conta (vinculada ao mesmo usuário)
   - [q] Logout

---

## 📌 Observações e próximos passos recomendados

- Persistência: atualmente os dados são mantidos em memória. Recomenda-se migrar para SQLite/SQLAlchemy para salvar clientes/contas entre execuções.
- Segurança: para produção, armazenar senhas com hashing (passlib) e proteger CPFs sensíveis.
- Reset diário de número de saques: implementar registro de data para reset automático por dia.
- Interface: considerar GUI (Tkinter/PyQt) para melhor usabilidade.
- Exportação: gerar relatórios/exportar extrato para CSV/Excel.

---

## 🛠️ Estrutura resumida (arquivos principais)

- app.py — lógica do menu e operações (atual)
- README.md — documentação (este arquivo)

---

Se desejar, posso:
- Gerar a versão com persistência SQLite/SQLAlchemy;
- Implementar reset diário de saques por data;
- Converter para GUI com Tkinter.  