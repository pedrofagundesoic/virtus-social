# Virtus: correções do app (documento único)

Substitui `SUGESTOES-APP.md`, `-2`, `-3` e `-4` (rodadas de 24/09, 29/09, 07/10 e 13/10/2026; o texto completo de cada uma continua no histórico do git).

**Última verificação:** 19/10/2026. Web desktop 1440×900 e celular 390×844; Android **v1.3.9** (Galaxy S25). Conta de testes com 15 ativos em 4 corretoras, compras de 2022–2023. Os números de proventos foram conferidos com o CSV exportado pelo próprio app e com fontes externas (Yahoo Finance; séries 433, 4389 e 13522 do Banco Central).

**Como usar:** a seção 1 é o que falta fazer. As seções 2 e 3 são histórico, para não reabrir o que já foi resolvido ou descartado.

---

## 1. Em aberto

### 🔴 1.1 Proventos registrados em dobro (novo, 19/10)

O CSV "Proventos recebidos" tem grupos com o **mesmo ativo, data-com, tipo e valor por cota** em duas datas de pagamento. Conferindo com os eventos da Yahoo, aparecem dois padrões de erro:

| Padrão | Exemplos (ativo · data-com · valor/cota → datas de pagamento) | A mais |
|---|---|---|
| Mesmo provento duas vezes, com 1–10 dias de diferença | ITSA4 · 18/06/2026 · 0,138 → 28/08 e 31/08/2026 · ITSA4 · 27/02/2026 · 0,024243 → 31/03 e 01/04/2026 · WEGE3 · 22/09/2023 → 12/03 e 13/03/2024 · MXRF11 · 30/09/2022 · 0,10 → 07/10 e 17/10/2022 · PETR4 · 27/04/2023 → 26/12 e 27/12/2023 | R$ 281,75 |
| Registro provisório com pagamento = data-com, mantido depois que saiu a data real | SAPR11 · 30/06/2025 → 30/06/2025 e 26/06/2026 · SAPR11 · 30/12/2025 → 30/12/2025 e 26/06/2026 · EGIE3 · 18/12/2025 → 18/12/2025 e 20/05/2026 · PETR4 (rendimento) · 16/04/2025 → 16/04 e 20/05/2025 · WEGE3 · 26/09/2025 → 12/12/2025 e 11/03/2026 | R$ 217,04 |

- **Total provável a mais:** **R$ 498,79** dos R$ 25.043,61 exibidos. Isso afeta "Total recebido", "Proventos (total)" de cada ativo, Top 5, calendário e YoC.
- **Não é erro:** PETR4 (dividendos e JCP de 2024–2026) e KLBN11 pagam **em parcelas** com a mesma data-com. O total do evento na Yahoo bate com a soma das parcelas.
- **Inconclusivo, para o desenvolvedor conferir na fonte oficial (B3/FNET, avisos da Itaúsa):** 4 grupos de ITSA4 com o mesmo JCP em duas datas, R$ 140,76 no total. As linhas estão abaixo, como vêm no CSV, com 600 ações.

  | Data-com | Valor/cota | Pago em | Pago de novo em | Por linha |
  |---|---|---|---|---|
  | 21/09/2023 | 0,1165 | 08/03/2024 | 30/12/2024 | R$ 69,90 |
  | 19/10/2023 | 0,0515 | 08/03/2024 | 30/12/2024 | R$ 30,90 |
  | 19/09/2024 | 0,0484 | 07/03/2025 | 30/04/2025 | R$ 29,04 |
  | 09/12/2025 | 0,0182 | 06/03/2026 | 30/04/2026 | R$ 10,92 |

  **O que consegui ver:**
  - Na Yahoo, cada data-com tem **um único evento**, com valor próximo do líquido de IR: 0,103143 para 0,1165 e 0,045596 para 0,0515. Isso sugere que o mesmo provento foi lançado duas vezes.
  - O padrão de datas (março e abril/dezembro) também pode ser JCP pago em duas parcelas, e a Yahoo pode juntar parcelas num evento só.
  - Não tenho como confirmar daqui.

  **Pergunta para o desenvolvedor:** a fonte (BRAPI) traz esses JCPs como duas parcelas de valor igual, ou como um evento só que foi gravado duas vezes, por exemplo uma data provisória e outra definitiva?

**Sugestão:**
- deduplicar por (ativo, data-com, tipo, valor/cota, data de pagamento ±10 dias);
- quando chegar a data de pagamento oficial, **substituir** o registro provisório em vez de criar outro.

### 🟡 1.2 Botão "+" cobre o campo de busca (Android)
Carteira → ao rolar até "Posições", o botão flutuante fica em cima de "Buscar ticker ou nome". É o item 6 do doc 1, que voltou com a busca nova. **Sugestão:** `padding` inferior na lista, ou esconder o botão enquanto o campo de busca estiver visível.

### 🟡 1.3 Corretora em branco num card (Android)
Carteira → BTLG11 aparece como "Fundos Imobiliários ·" sem a corretora. No CSV e no site é **NuInvest**.

### 🟡 1.4 Abreviação de corretora nos filtros (Android)
Os filtros de instituição mostram `NUINV`. No site e no CSV o nome já é **NuInvest**.

### 🟡 1.5 Ponto decimal nos indicadores (web)
Detalhe do ativo: `P/L 8.89`, `P/VP 7.50` com ponto, ao lado de `DY 11,00%` com vírgula. No Android isso já foi corrigido.

### 🟡 1.6 Duas médias no mesmo gráfico (web)
Proventos → Fluxo de proventos: a linha diz **"média R$ 498,3/mês"** e a legenda diz **"Média do período R$ 501,87"**. São 5.979,72 ÷ 12 (meses fechados) contra 6.022,47 ÷ 12 (365 dias). Usar uma só.

### ⚪ 1.7 Não verificados desde 24/09
Doc 1:
- **#3:** cotação "—" logo após o cadastro.
- **#4:** campo de data que rejeita barras.
- **#5:** limite para percentuais fora da realidade.
- **#13:** a data volta para "hoje" a cada lançamento.
- **#14:** a tela recarrega inteira depois de salvar.

Doc 2:
- **#10:** data cortada em "Pagamentos recentes" no celular.

Ficam para quando houver tempo de testar o cadastro.

---

## 2. Resolvido (para não reabrir)

| Item | Resolvido em | Como ficou |
|---|---|---|
| Lançamento ia sempre para a carteira padrão | 07/10 | Campo "Carteira" no formulário |
| Gerenciar carteiras | 07/10 | Renomear, definir padrão e excluir em Conta |
| "Editar ordens" escondido | 07/10 | Seção Movimentações no detalhe do ativo |
| Busca e ordenação de posições | 07/10 | Web e Android |
| Legenda do Mapa de Dividendos | 07/10 | "Quanto mais vivo o verde…" |
| Metodologia do "95% de acerto" | 07/10 | Link "como calculamos": 3345 ÷ 3512 |
| Cabeçalho da Watchlist | 07/10 | Compacto |
| Exportar dados | 07/10 | 3 CSVs em Conta |
| Gráfico de 12 meses com degrau / "411% do CDI" | 13/10 | Curva contínua, +32 a 35% (bate com as cotações reais) |
| YoC da carteira 0,06% | 13/10 | 9,79% |
| Virtus IR com dividendos zerados | 13/10 → 19/10 | R$ 1.490,00 / JCP R$ 1.272,84, iguais ao CSV |
| "Recebido últimos 12M" R$ 36,95 / proventos do mês R$ 0,00 | 13/10 | Corretos |
| Fluxo de renda (sankey) cortado no celular / rótulos sobrepostos | 13/10 | Lista no celular, sem sobreposição |
| Calendário do Android cortando valores | 13/10 | Valores completos |
| Três totais de 12 meses diferentes | 19/10 | 365 dias = R$ 6.022,47 em todo lugar; o calendário diz a janela ("nov/25–out/26") |
| Projeção 12M abaixo do histórico | 19/10 | R$ 6.134,26, com a fórmula explicada na tela |
| CSV de posições sem proventos / com abreviações | 19/10 | Preenchido; "BTG Pactual", "NuInvest" |
| Ponto decimal e data ISO no Android | 19/10 | Vírgula e dd/mm/aaaa |
| Patrimônio vazando do card (web, celular) | 19/10 | Cabe |
| E-mail no rodapé da barra lateral (web) | 19/10 | Só "Plano Premium" |
| Rótulo do IPCA no período "Mês" | 19/10 | "IPCA set/26" |
| "Prováveis Pagadores" com 80 mil px no celular | 13/10 | Filtro "Só minha carteira" |

## 3. Conferido e descartado (não era erro)

| Suspeita | Por que não era erro |
|---|---|
| Período "Mês" com IBOV +9,99% e carteira +7% (07/10) | Ibovespa real +9,66% na semana; carteira recalculada com cotações reais: +6,96% |
| IPCA +0,82% no mês (13/10) | É o IPCA de set/2026 divulgado pelo IBGE (0,82%, série 433 do BCB) |
| Gráfico do mês com salto no início (13/10) | O Ibovespa subiu 7,7% num único dia (05/10) |
| "Contexto macro": Selic 13,75%, IPCA 12m 4,58%, CDI 13,65% (19/10) | IPCA 12m e CDI conferem com as séries 13522 e 4389 do BCB |
| PETR4 e KLBN11 com o mesmo provento pago 2–3 vezes (19/10) | São parcelas de um mesmo evento |
