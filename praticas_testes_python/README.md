# Aula 2 — Prática de Testes Unitários em Python (4 práticas)

Pacote autocontido: **4 mini-projetos novos**, cada um com o código e os testes bem comentados.
Tudo foi executado e conferido antes de ser entregue.

```
praticas_testes_python/
├── README.md                  ← este roteiro
├── requirements.txt           ← pytest
├── pytest.ini                 ← registra a marca "gui"
├── pratica1_boletim/          ← boletim.py + test_boletim.py
├── pratica2_senha/            ← validador_senha.py (COM BUG) + test_validador_senha.py
├── pratica3_conta/            ← conta.py + test_conta.py
├── pratica4_conversor/        ← conversor.py + app.py (Tkinter) + test_conversor.py
└── gabarito/validador_senha_corrigido.py
```

## 0. Antes da aula (professor, 10 min)
1. Python **3.10 ou superior** instalado (`python --version`). No Windows o Tkinter já vem junto; no Linux: `sudo apt install python3-tk`.
2. Descompacte o zip numa pasta sem acentos/espaços (ex.: `C:\aulas\praticas_testes_python`).
3. Rode UMA vez a sequência da seção 1 para garantir que tudo funciona no laboratório.

## 1. Preparar o ambiente (todos os alunos, 30–45 min)
Abra o terminal **dentro da pasta** `praticas_testes_python`.

**Windows (cmd ou PowerShell)**
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest --version
```
Esperado: `pytest 9.x.x` (qualquer versão ≥ 8 serve). O prompt passa a mostrar `(.venv)`.

> Se o PowerShell bloquear o `activate`: `Set-ExecutionPolicy -Scope Process RemoteSigned` e tente de novo.
> Se `pytest` não for reconhecido: use `python -m pytest` no lugar de `pytest` em todos os comandos.

### Como ler a saída do pytest
| Símbolo | Significa |
|---|---|
| `.` | teste passou |
| `F` | teste falhou (veja o trecho `assert` e a seta `>` indicando a linha) |
| `s` | teste pulado (skip) |
| `14 passed in 0.03s` | resumo final |

Comandos úteis: `pytest -v` (um teste por linha) · `pytest -x` (para no 1º erro) · `pytest -k borda` (só testes com "borda" no nome) · `pytest -m "not gui"` (sem janela real).

## 2. Prática 1 — Boletim (1h30) · funções puras
**Conceitos:** padrão AAA, `pytest.approx`, `pytest.raises`, `parametrize`, valor limite.

1. Abra `boletim.py` e leia as regras (≥ 6 aprova; ≥ 4 recuperação).
2. Entre na pasta e rode: `cd pratica1_boletim` → `pytest -v`. Esperado: **14 passed**.
3. Leia `test_boletim.py` de cima para baixo (os comentários explicam o porquê de cada técnica).
4. **Experimento (5 min):** em `boletim.py` troque `media >= MEDIA_APROVACAO` por `media > MEDIA_APROVACAO` e rode de novo. Quais testes falham? (os de **borda**: 6.0 e o fluxo completo). Desfaça a troca. *Lição: a borda pega o erro que o teste "do meio" não pega.*
5. **Exercício dos alunos:** escrever um teste novo para `calcular_media([10, 10, 10])` e um para `situacao(7)`.

## 3. Prática 2 — Caça ao bug (1h30) · defeito, relatório e regressão
**Conceitos:** tabela de casos, valor limite, ciclo de vida do defeito, teste de regressão.

1. `cd pratica2_senha` → `pytest -v`.
2. Esperado na 1ª execução: **1 failed, 10 passed** — falha em
   `test_tamanho_minimo_na_borda[Abcdef1!-True]` (senha de exatamente 8 caracteres recusada).
3. **Não corrija ainda.** Peça aos alunos que preencham o relatório de defeito (modelo na seção 7).
4. Dê 10 min para acharem a linha em `validador_senha.py` (dica: leia a regra no docstring e compare com o `if` do tamanho).
5. Correção: `<=` → `<` na linha `if len(senha) <= TAMANHO_MINIMO:`. Versão pronta em `gabarito/validador_senha_corrigido.py`.
6. Rode de novo: **11 passed**. Isso é o **teste de regressão**: o mesmo teste que achou o bug agora o protege para sempre.
7. Discussão: por que a senha longa passou e a de 8 caracteres não? (Onde o bug mora: na borda.)

## 4. Prática 3 — Conta bancária (1h30) · estado, fixtures, exceções
**Conceitos:** fixture, isolamento entre testes, exceção própria, "efeito colateral", encapsulamento (`property`).

1. `cd pratica3_conta` → `pytest -v`. Esperado: **12 passed**.
2. Mostre a fixture `conta`: cada teste recebe uma conta nova (Ana, saldo 100).
3. Ponto-chave: `test_transferencia_sem_saldo_nao_credita_o_destino` — não basta a exceção acontecer; **nada pode ter mudado** nas duas contas.
4. **Experimento:** em `conta.py`, no método `sacar`, mova a linha `self._saldo -= valor` para ANTES da verificação de saldo. Quais testes falham? Desfaça.
5. O teste para `ContaBancaria("Dani", 50).sacar(0)` está em `test_conta.py`: saque zero deve levantar `ValueError` sem alterar o saldo.

## 5. Prática 4 — Conversor desktop (1h30) · testar Tkinter
**Conceitos:** separar lógica de interface, `Mock`, `patch`, `__new__`, GUI real com `invoke()`.

1. Execute o programa para ver a janela: `cd pratica4_conversor` → `python app.py` (digite 100 → `212.0 °F`).
2. Rode os testes: `pytest -v`. Esperado: **14 passed** (com tela) ou **13 passed, 1 skipped** (sem tela).
3. Percorra os 3 níveis em `test_conversor.py`:
   - **A — lógica pura:** `conversor.py` não importa tkinter; testes em milissegundos.
   - **B — interface com dublês:** `AppConversor.__new__` pula o `__init__` (que abriria janela); `Mock` imita os widgets; `patch("app.messagebox")` impede o pop-up.
   - **C — janela real:** `botao.invoke()` clica sem `mainloop()`. Só 1 teste: é o mais lento e frágil.
4. **Experimento:** em `conversor.py`, troque `.replace(",", ".")` por `.replace(";", ".")` e rode. Qual teste acusa? (o da vírgula decimal).
5. O teste para `converter_texto("0")` está em `test_conversor.py` e verifica o resultado `"32.0 °F"`.

## 6. Fechamento (30 min)
Rode tudo na raiz: `pytest -m "not gui"` (a Prática 2 só fica 100% verde depois da correção).
Cada aluno preenche o **relatório de teste** (seção 7) e entrega prints dos 4 resultados.

## 7. Modelos
**Relatório de defeito**
| Campo | Preencher |
|---|---|
| ID / Título | BUG-001 · Senha de 8 caracteres é recusada |
| Passos | 1) `validar_senha("Abcdef1!")` 2) conferir a lista de problemas |
| Esperado × Obtido | `[]` (válida) × `["Use no mínimo 8 caracteres."]` |
| Severidade / Prioridade | Alta / Alta (bloqueia cadastros legítimos) |
| Evidência | print do `pytest` com o `F` |
| Status | Aberto → Corrigido → Fechado (após regressão) |

**Relatório de teste (por prática):** executados · aprovados · reprovados · taxa de aprovação (= aprovados ÷ executados × 100) · decisão.
Ex.: Prática 2 na 1ª execução → 11 executados, 10 aprovados, 1 reprovado → **90,9%** → corrigir antes de liberar.

## 8. Solução de problemas
| Sintoma | Causa / solução |
|---|---|
| `ModuleNotFoundError: boletim` | você rodou `pytest` fora da pasta da prática; faça `cd` para ela |
| `pytest: command not found` | ambiente não ativado, ou use `python -m pytest` |
| `ModuleNotFoundError: tkinter` (Linux) | `sudo apt install python3-tk` |
| Teste GUI "skipped" | computador sem tela (SSH/servidor). Normal; em Linux use `xvfb-run pytest` |
| Janela aparece e some durante o teste | é o teste C (GUI real) rodando; é esperado |
