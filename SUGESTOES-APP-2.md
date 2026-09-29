# Virtus: correções sugeridas (2ª rodada)

**Contexto:** observações de 29/09/2026 na conta de testes. A carteira foi zerada e recadastrada do zero com 15 ativos (9 ações BR e 6 FIIs) em 4 corretoras (XP, BTG, NuInvest, Inter), com compras datadas entre fev/2022 e set/2023. Plataformas usadas:
- **Web:** desktop 1440×900 e celular 390×844, em virtusapp.com.br.
- **Android:** app nativo em um Galaxy S25.

Estes itens são **novos** e não repetem os 15 do primeiro documento (`SUGESTOES-APP.md`). Estão ordenados por impacto.

Números de referência da própria conta, usados para comparar as telas:

| Indicador | Valor | Onde aparece |
|---|---|---|
| Valor aplicado | R$ 61.508,50 | Carteira (web) |
| Proventos recebidos (histórico) | R$ 24.125,68 | Carteira e Proventos (web e Android) |
| Proventos, últimos 12 meses | R$ 5.811,14 / R$ 5.811,16 | Proventos (web) / Carteira (web) |
| Proventos recebidos em set/2026 | R$ 768,55 | Proventos → Por mês (web) |

---

## 🔴 Números errados ou incoerentes

### 1. "YoC" do card "Renda (12 meses)" mostra 0,06%

**Onde:** Web → Carteira, card **Renda (12 meses)**, linha pequena abaixo do valor.

**O que acontece:** o card mostra `R$ 5.811,16` e, logo abaixo, `YoC 0,06%`. Com R$ 61.508,50 aplicados, o esperado é algo perto de **9,4%** (5.811,16 ÷ 61.508,50). No detalhe de um ativo o YoC está certo (BBSE3: `16,45%`), então o erro está só no agregado da carteira.

**Sugestão:** conferir a fórmula do agregado. Provavelmente há unidade trocada (fração × percentual) ou o divisor errado. Enquanto não estiver certo, vale esconder a linha.

---

### 2. Virtus IR: "Dividendos no ano" zerado e "JCP bruto no ano" muito abaixo do recebido

**Onde:** Web → Virtus IR.

**O que acontece:**

```
Dividendos no ano     R$ 0,00
JCP bruto no ano      R$ 36,95
```

A própria lista de proventos da conta mostra, só em 2026, vários pagamentos que deveriam entrar aqui. Alguns exemplos:
- **Dividendos:** BBSE3 `R$ 509,99` (02/03/2026) e `R$ 396,66` (03/09/2026); VALE3 `R$ 27,72` (02/09/2026); KLBN11 `R$ 34,20` (19/08/2026); WEGE3 `R$ 33,03` (12/08/2026).
- **JCP:** PETR4 `R$ 70,10` (20/08 e 21/09/2026); ITSA4 `R$ 82,80` e `R$ 69,60` (31/08/2026); TAEE11 `R$ 83,85` (26/08/2026); VALE3 `R$ 94,12` (02/09/2026).

**Suspeita:** o valor `R$ 36,95` também aparece no item 3, em outra tela. Parece que as duas telas leem a mesma consulta, e essa consulta ignora proventos gerados para compras com data retroativa (as compras foram lançadas hoje, com datas de 2022 e 2023).

**Por que importa:** é a tela que o usuário vai usar para declarar imposto. Um valor zerado ali é pior do que não ter a tela.

---

### 3. Android → Proventos → "Projeção 12 meses": "Recebido últimos 12M" = R$ 36,95

**Onde:** app Android → aba **Proventos** → card **Projeção 12 meses**.

**O que acontece:** `RECEBIDO ÚLTIMOS 12M: R$ 36,95`. Na mesma aba, o calendário de proventos diz `Total 12m: R$ 5.811,16`, e o site mostra `R$ 5.811,14`. A projeção (`R$ 401,57`) parece herdar o mesmo erro, porque fica muito abaixo do histórico de 12 meses.

**Sugestão:** usar a mesma fonte do calendário/fluxo de 12 meses. Ver também a suspeita do item 2.

---

### 4. Android → Análises → Rentabilidade (período "Mês"): "Proventos R$ 0,00"

**Onde:** app Android → aba **Análises** → card **Rentabilidade** → período **Mês**.

**O que acontece:**

```
+0.05%   +R$ 36,65
Aportes R$ 0,00 · Proventos R$ 0,00 · Valor atual R$ 68.485,70
De 2026-09-01 até 2026-09-29
```

Em setembro a conta recebeu **R$ 768,55** em proventos (web → Proventos → Por mês). "Aportes R$ 0,00" está correto, porque não houve compra no mês.

**Detalhe de formatação na mesma tela:** os percentuais usam ponto (`+0.05%`, `+1.03%`) e a data vem em ISO (`2026-09-01`). O resto do app usa vírgula e `dd/mm`.

---

### 5. Gráfico "Rentabilidade · 12 meses" com degrau vertical (Android)

**Onde:** app Android → aba **Carteira** → card **Rentabilidade · 12 meses**.

**O que acontece:** a linha da carteira sobe na vertical no meio do período, como se o patrimônio inteiro tivesse "entrado" num único dia. Todas as compras são de 2022 e 2023, então nos 12 meses exibidos a carteira já existia inteira. No site, com a mesma carteira, o gráfico sai contínuo (`+11,46%`).

**Suspeita:** o Android monta a série pela data de *cadastro* dos lançamentos (hoje), e não pela data da operação. O mesmo degrau aparecia no site logo depois do primeiro cadastro, com um só ativo (ITSA4): `+330,22%` no gráfico.

---

### 6. Pequena divergência entre "Renda (12 meses)" e "Últimos 12 meses"

**Onde:** Web → Carteira mostra `R$ 5.811,16`. Web → Proventos mostra `R$ 5.811,14`.

**Sugestão:** uma única função de soma (ou o mesmo arredondamento) para os dois cards. A diferença é de centavos, mas é o tipo de coisa que o usuário nota e que tira a confiança nos outros números.

---

## 🟡 Layout e legibilidade

### 7. "Fluxo de renda" (sankey) cortado no site em tela de celular

**Onde:** web em celular (largura 390 px) → Proventos → **Fluxo de renda · 12 meses**.

**O que acontece:** só a metade esquerda aparece (Dividendos / JCP / Rendimentos). O nó central e os ativos à direita ficam fora do card, sem rolagem horizontal.

**Sugestão:** em telas estreitas, girar o diagrama para vertical ou trocar por uma lista "tipo → ativos". Outra opção é permitir rolagem horizontal dentro do card.

---

### 8. Rótulos sobrepostos no "Fluxo de renda" (desktop)

**Onde:** web desktop → Proventos → **Fluxo de renda**.

**O que acontece:** quando dois ativos têm fatias pequenas e vizinhas, os rótulos se sobrepõem. Na conta de testes, `TAEE11 · R$ 426,3` fica embaixo de `VALE3 · R$ 336,8`.

**Sugestão:** distância mínima entre rótulos (empurrar para baixo) ou juntar em "Outros" as fatias abaixo de um limite.

---

### 9. Calendário de proventos do Android corta os valores

**Onde:** app Android → Proventos → **Calendário de proventos · 12 meses**.

**O que acontece:** os quadrados dos meses cortam o valor: `R$ 190,0`, `R$ 993,2`, `R$ 460,9`, `R$ 303,5`.

**Sugestão:** reduzir a fonte automaticamente, abreviar (`R$ 993` ou `R$ 1,0 mil`) ou usar 3 colunas em vez de 4.

---

### 10. Data dos pagamentos recentes cortada no site em tela de celular

**Onde:** web em celular → Proventos → **Pagamentos recentes**.

**O que acontece:** a linha vira `Rendimento · 25 de set. de ...`. O ano some, e é justamente a parte que diferencia um pagamento deste ano de um do ano passado.

**Sugestão:** usar data curta no celular (`25/09/26`) ou quebrar em duas linhas.

---

### 11. Nome da corretora abreviado de formas diferentes

**Onde:**
- Web → Análises → "Por instituição" mostra `NUINV`.
- Android → Carteira → filtros de instituição mostra `NUIN` (chip cortado; ver também o item 12 do primeiro documento).
- No formulário de cadastro a mesma instituição aparece com o nome completo, `NuInvest`.

**Sugestão:** usar sempre o nome de exibição (`NuInvest`), com abreviação só se faltar espaço, e a mesma nas duas plataformas.

---

## 📌 Resumo em uma linha por item

| # | Item | Onde | Tipo |
|---|---|---|---|
| 1 | YoC da carteira mostra 0,06% (esperado ≈ 9,4%) | Web · Carteira | 🔴 Número |
| 2 | Virtus IR: dividendos no ano R$ 0,00 e JCP R$ 36,95 | Web · Virtus IR | 🔴 Número |
| 3 | Projeção 12 meses: "Recebido últimos 12M" R$ 36,95 | Android · Proventos | 🔴 Número |
| 4 | Rentabilidade do mês com "Proventos R$ 0,00" | Android · Análises | 🔴 Número |
| 5 | Gráfico de 12 meses com degrau vertical | Android · Carteira | 🔴 Número |
| 6 | R$ 5.811,16 × R$ 5.811,14 para o mesmo indicador | Web | 🔴 Número |
| 7 | Sankey "Fluxo de renda" cortado no celular | Web mobile · Proventos | 🟡 Layout |
| 8 | Rótulos sobrepostos no sankey | Web desktop · Proventos | 🟡 Layout |
| 9 | Calendário de proventos corta os valores | Android · Proventos | 🟡 Layout |
| 10 | Data dos pagamentos recentes cortada | Web mobile · Proventos | 🟡 Layout |
| 11 | "NUINV" / "NUIN" / "NuInvest" para a mesma corretora | Web e Android | 🟡 Layout |

**Pista comum dos itens 2, 3, 4 e 5:** todos envolvem compras cadastradas hoje com data de operação antiga. Vale testar se essas consultas filtram pela data de criação do registro em vez da data da operação ou da data do provento.
