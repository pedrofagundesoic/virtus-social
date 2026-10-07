# Virtus: verificação das correções e novos pontos (3ª rodada)

**Contexto:** verificação feita em 07/10/2026 na mesma conta de testes das rodadas anteriores (15 ativos, 4 corretoras, compras de 2022–2023). Plataformas:
- **Web:** desktop 1440×900 e celular 390×844.
- **Android:** app **v1.3.5** num Galaxy S25.

Este documento tem três partes:
1. o que **foi corrigido**;
2. o que **ainda não foi**, com o estado atual;
3. **pontos novos**, incluindo uma regressão.

**Conferido e descartado:** os números de Análises → Rentabilidade → **Mês** do Android estão **corretos**. A carteira subiu `+7.00% / +R$ 4.867,00` de 01/10 a 07/10, e pelas cotações reais a conta dá **+6,96% / +R$ 4.836**. O Ibovespa subiu **+9,66%** desde o fechamento de 30/09 (o app mostra +9,99%), com alta de 7,7% em 05/10. O dólar caiu −3,24% (app: −3,62%) e o S&P 500 subiu +1,96% (app: +1,91%). As pequenas diferenças são de horário da cotação. Nessa tela continuam valendo só o item 4 do doc 2 (proventos do mês R$ 0,00) e a formatação (ponto e data ISO).

"Não verificado" quer dizer que o teste exigiria criar ou apagar lançamentos, o que não fiz desta vez.

---

## ✅ Corrigido (obrigado!)

| Doc | # | Item | Como está agora |
|---|---|---|---|
| 1 | 2 | Gerenciar carteiras | Web → Conta → "Suas sub-carteiras": renomear, definir padrão (estrela) e excluir, com o aviso "ao excluir, os lançamentos vão para a carteira padrão" |
| 1 | 7 | "Editar ordens" escondido | O detalhe do ativo mostra a seção **Movimentações** com a lista de ordens e "Toque numa ordem para corrigir ou excluir" (Android e web) |
| 1 | 8 | Busca e ordenação | "Buscar ticker ou nome" e "Ordenar: A–Z · Valor · Rentabilidade · Proventos" na web e no Android |
| 1 | 9 | Legenda do Mapa de Dividendos | O texto agora diz "Quanto mais vivo o verde da célula, mais frequente", coerente com a escala (web) |
| 1 | 10 | Metodologia do "95% de acerto" | Link "como calculamos" ao lado da afirmação |
| 1 | 11 | Cabeçalho da Watchlist | Compacto com 1 ativo; com 5 ativos mostra as fontes das cotações (BRAPI PRO ~5 min, Yahoo ~15 min) |
| 1 | 15 | Exportar dados | Web → Conta → "Planilhas CSV": posições, lançamentos e proventos |
| 1 | 1 | Lançamento na carteira errada | O formulário tem o campo **Carteira** ("Vai para a carteira"). A pré-seleção pela carteira ativa não foi testada |

---

## 🔴 Ainda não corrigido

### Do 2º documento (`SUGESTOES-APP-2.md`)

| # | Item | Como está em 07/10 |
|---|---|---|
| 1 | YoC da carteira | Web → Carteira → "Renda (12 meses) R$ 5.843,01" continua com **`YoC 0,06%`**. Com R$ 61.508,50 aplicados, o esperado é ≈ **9,5%** |
| 2 | Virtus IR | Continua **"Dividendos no ano R$ 0,00"** e **"JCP bruto no ano R$ 36,95"**. A lista de proventos da própria conta mostra vários dividendos e JCP pagos em 2026 |
| 3 | "Recebido últimos 12M" (Android) | Continua **R$ 36,95** na "Projeção 12 meses". Na mesma aba, o calendário diz "Total 12m: R$ 5.843,01" |
| 4 | Análises → Rentabilidade → Mês (Android) | "Proventos **R$ 0,00**" de 01/10 a 07/10, mas a conta recebeu R$ 14,55 (ITSA4, JCP, 01/10). Os percentuais continuam com ponto (`+7.00%`) e a data em ISO (`2026-10-01`) |
| 5 | Degrau no gráfico de 12 meses | **Continua no Android e agora aparece também na web** (ver o novo item A) |
| 6 | Dois valores para "renda de 12 meses" | **Piorou:** Carteira mostra **R$ 5.843,01**, Proventos mostra **R$ 6.018,94** (diferença de R$ 175,93) |
| 7 | Sankey cortado no celular (web) | Igual: só aparece a coluna da esquerda |
| 8 | Rótulos sobrepostos no sankey (desktop) | Igual: `TAEE11 · R$ 516,6` encosta em `VALE3 · R$ 336,8` |
| 9 | Calendário do Android corta valores | Igual: `R$ 460,9…`, `R$ 993,2…`, `R$ 968,5…` |
| 10 | Data cortada em "Pagamentos recentes" (celular) | Igual: `Rendimento · 25 de set. de …` |
| 11 | Nome da corretora | Web → Análises → "Por instituição" continua `NUINV` |

### Do 1º documento (`SUGESTOES-APP.md`)

| # | Item | Como está em 07/10 |
|---|---|---|
| 6 | Botão "+" cobre conteúdo | Android → Carteira: o botão flutuante ainda cobre o selo de rentabilidade do card do meio da tela (ex.: EGIE3) |
| 5 | Percentuais fora da realidade | O card mostra **"411% do CDI"** (+59,34% contra CDI +14,45%). A conta está certa, mas o +59% vem do degrau do item A. Sem limite ou aviso, o número parece defeito |
| 3, 4, 12, 13, 14 | Cotação "—", campo de data, chip cortado, data padrão, recarregamento | Não verificados nesta rodada |

---

## 🆕 Pontos novos

### A. 🔴 Regressão: o gráfico "Rentabilidade · 12 meses" da web agora também tem o degrau

**Onde:** Web → Carteira → **Rentabilidade · 12 meses** (e o mesmo gráfico no Android).

**O que acontece:**
- **Em 29/09** o gráfico da web era contínuo e mostrava **+11,46%**.
- **Hoje** ele tem um salto vertical no meio do período e mostra **+59,37%** (Android: **+59,34% / R$ 34.276,35**, "**411% do CDI**").
- O salto fica perto de **07/04/2026**. No tooltip do Android a carteira está em **+18,51%** nesse dia e, logo depois, perto de **+50%**.

**Conferência com cotações reais:** recalculei o valor da carteira de testes dia a dia, com as cotações de fechamento da B3 (Yahoo Finance) e as quantidades da conta.

| | Valor real calculado | O que o Virtus mostra |
|---|---|---|
| Variação de preço em 12 meses (07/10/2025 → 07/10/2026) | **+22,99%** (+R$ 13.890) | +59,34% (+R$ 34.276) |
| Mesmo somando os R$ 5.843 de proventos de 12 meses | ≈ +32,7% (+R$ 19.733) | |
| Carteira em 07/04/2026 | +19,5% | +18,51% (bate) |
| Maior alta de um dia no período | +4,43% (19/01/2026) | salto de ~30 p.p. perto de 07/04 |
| De 06/04 a 08/04/2026 | +0,6% | ~+30 p.p. |

Até o salto a série confere com o mercado. No salto não aconteceu nada no mercado nem na carteira, já que todas as compras são de 2022 e 2023.

**Por que é crítico:**
- É o primeiro gráfico da tela inicial.
- O valor final mostra quase o triplo do rendimento real.
- Esse valor alimenta o "% do CDI".

**Hipótese para investigar:** o tamanho do salto (~30 p.p. de ~R$ 60 mil, ou seja, ~R$ 18 mil) é próximo dos **R$ 18.888 em proventos recebidos antes da janela de 12 meses** (R$ 24.906,88 no histórico − R$ 6.018,94 nos últimos 12 meses). Pode ser que, a partir de algum ponto, a série passe a somar todos os proventos desde a 1ª compra, e não só os do período.

---

### B. 🟡 Formato de número misturado nos "Indicadores fundamentalistas"

**Onde:** Android → detalhe do ativo → **Indicadores fundamentalistas**, e o card de indicadores no detalhe do ativo na web.

**O que acontece:**
- **Android:** `P/L 8.66`, `DIVIDEND YIELD 11.00%`, `ROE 84.38%` usam ponto. A fonte aparece como `atualizado 2026-10-06T21:51:44.326554Z`, um timestamp técnico.
- **Web:** `DY 11,00%` e `ROE 84,38%` usam vírgula.

**Sugestão:** formatação pt-BR em todo lugar (`8,66` · `11,00%`) e data legível (`atualizado em 06/10, 18:51`).

---

### C. 🟡 "Prováveis Pagadores" tem uma página muito longa no celular

**Onde:** web no celular → Proventos → **Prováveis Pagadores**.

**O que acontece:** com 26 anunciados e 277 prováveis, a página passa de **80 mil pixels de altura** (cerca de 95 telas de celular). Quem quer saber só dos ativos da própria carteira rola muito antes de achar.

**Sugestão:**
- deixar o filtro **"Só minha carteira"** ativo por padrão para quem tem posições;
- recolher "Prováveis" e mostrar só os "Anunciados" de início, com "ver mais".

---

## 📌 Prioridade sugerida

1. **A** (regressão do gráfico, que afeta também o "% do CDI").
2. **Doc 2 #1, #2, #3 e #6:** números de proventos que não batem entre si (YoC, Virtus IR, "Recebido 12M", R$ 5.843,01 × R$ 6.018,94). Provavelmente têm causa comum: algumas consultas ignoram proventos de compras lançadas com data retroativa.
3. Layout: sankey no celular, calendário do Android, data cortada, botão "+" e formato de números.
