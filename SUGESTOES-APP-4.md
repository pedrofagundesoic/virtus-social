# Virtus: verificação das correções (4ª rodada)

**Contexto:** verificação feita em 13/10/2026 na mesma conta de testes (15 ativos, 4 corretoras, compras de 2022–2023). Plataformas:
- **Web:** desktop 1440×900 e celular 390×844, já com o layout novo.
- **Android:** app **v1.3.6** num Galaxy S25.

Para os números de proventos, a conferência usou o CSV "Proventos recebidos" exportado pelo próprio app (506 linhas, total R$ 24.906,91).

---

## ✅ Corrigido desde a 3ª rodada

| Origem | Item | Como está agora |
|---|---|---|
| Doc 3 · A | Degrau no gráfico "Rentabilidade · 12 meses" | Curva contínua nas duas plataformas. Web: **Carteira +34,83%** × Ibovespa +45,81%. Android: **+34,85% · 242% do CDI**. Bate com o cálculo por cotações reais (+23% de preço mais os proventos do período) |
| Doc 2 · 1 | YoC da carteira | **YoC 9,79%** (6.018,94 ÷ 61.508,50 = 9,79% ✔) |
| Doc 2 · 2 | Virtus IR | **Dividendos no ano R$ 1.489,99 · JCP bruto R$ 1.272,83.** Pelo CSV, 2026 tem R$ 1.490,00 em dividendos e R$ 1.272,84 em JCP ✔ |
| Doc 2 · 3 | "Recebido últimos 12M" (Android) | **R$ 6.018,94** ✔ |
| Doc 2 · 4 | Proventos do mês em Análises (Android) | **R$ 14,55** (ITSA4, 01/10) ✔ |
| Doc 2 · 7 | Fluxo de renda cortado no celular (web) | Virou uma lista "De onde vem / Quem paga", legível ✔ |
| Doc 2 · 8 | Rótulos sobrepostos no sankey (desktop) | Os rótulos não se sobrepõem mais ✔ |
| Doc 2 · 9 | Calendário do Android cortando valores | Valores completos (`R$ 460,92`, `R$ 993,21`) ✔ |
| Doc 2 · 11 | `NUINV` em Análises | Mostra **NuInvest** ✔ (ver item 4 abaixo, sobre o CSV) |
| Doc 3 · C | "Prováveis Pagadores" muito longa | Filtro **"Só minha carteira (7)"** e página de 2.365 px no celular (antes eram 80 mil) ✔ |
| Doc 1 · 6 | Botão "+" cobrindo conteúdo (Android) | Não se repetiu na lista de posições |

---

## 🔴 Ainda não corrigido / inconsistente

### 1. Três valores diferentes para a "renda dos últimos 12 meses"

| Onde | Valor |
|---|---|
| Web → Carteira, Web → Proventos, Android → Projeção 12 meses | **R$ 6.018,94** |
| Web → Proventos → Fluxo de renda ("Renda · 12 meses") | **R$ 6.018,97** |
| Android → Proventos → Calendário ("Total 12m") | **R$ 5.843,01** |

Conferindo pelo CSV exportado:
- **meses fechados nov/25–out/26** somam **R$ 5.843,02**, que é o "Total 12m" do calendário;
- **os últimos 365 dias** somam **R$ 6.018,97**, que é o valor do Fluxo de renda.

O R$ 6.018,94 dos outros cards é a mesma janela de 365 dias, com arredondamento diferente (3 centavos).

Então a diferença grande vem da janela: um soma meses fechados e o outro soma 365 dias corridos. **Sugestão:** escolher uma janela e usar em todo lugar, ou escrever a janela no rótulo ("nov/25–out/26" × "últimos 365 dias").

### 2. "Projeção próximos 12M" menor que o recebido nos últimos 12 meses (Android)

Android → Proventos → **Projeção 12 meses**: `Recebido últimos 12M R$ 6.018,94` e `Projeção próximos 12M R$ 3.491,93`. O texto diz "Estimativa baseada nos últimos 12 meses + proventos já anunciados". Com a mesma carteira, uma projeção 42% abaixo do histórico parece somar só o que já foi anunciado (+ parte dos meses). Vale revisar a fórmula ou explicar na tela por que a projeção é menor.

### 3. Formatação: ponto decimal e data ISO no Android (parcial)

- Análises → Rentabilidade: o número grande já usa vírgula (`+7,60%`), mas os cards de comparação continuam com ponto (`+0.41%`, `+10.96%`, `Carteira +7.19 p.p.`).
- O tooltip do gráfico de 12 meses mostra a data em ISO (`2026-04-13`).

### 4. CSV de posições com dados incompletos

Web → Conta → **Posições · CSV**:
- a coluna **"Proventos recebidos" vem `0` em todos os 15 ativos**, enquanto "Proventos 12m" está preenchida (ex.: BBSE3 `0` × `918,02`; o app mostra R$ 3.205,36 de total para BBSE3);
- a coluna **"Instituição"** usa as abreviações (`NUINV`, `INTER`, `BTG`), não o nome de exibição.

---

## 🆕 Pontos novos

### A. 🟡 Valor do patrimônio vaza do card na web em tela de celular

**Onde:** web no celular (390 px) → Carteira.

**O que acontece:** `R$ 74.732,55` (Patrimônio) e `+R$ 38.130,93` (Resultado total) passam da borda direita dos cards, que estão em 2 colunas. Com patrimônio de 6 dígitos ou mais, vai cortar.

**Sugestão:** fonte responsiva (`clamp`) ou 1 coluna abaixo de ~400 px.

### B. ⚪ IPCA do período "Mês" (Android): valor correto, falta dizer de qual mês é

Análises → Rentabilidade → **Mês** (01/10 a 13/10) mostra `IPCA +0.82%`. **O número está certo:** é o IPCA de setembro/2026 divulgado pelo IBGE (0,82%, conferido na série 433 do Banco Central), já que o de outubro ainda não saiu. Só falta deixar isso claro, por exemplo com o rótulo "IPCA set/26 (último divulgado)", para o usuário não achar que é a inflação dos 13 dias de outubro.

### C. 🟡 Gráfico de comparação do período "Mês" (Android) começa com salto

Análises → Gráfico de rentabilidade (IBOV, Mês): a linha do IBOV sai de 0 e sobe quase tudo no primeiro ponto, depois fica plana. O número final (+10,45%) bate com o mercado, mas o desenho sugere que o primeiro ponto está sem valor (base zero) em vez de começar no fechamento de 30/09.

### D. ⚪ Observação: e-mail do usuário visível no rodapé da barra lateral (web)

O novo rodapé da barra lateral mostra `Premium · <e-mail>`. Não é bug, mas aparece em qualquer print ou compartilhamento de tela. Talvez mostrar só o nome e deixar o e-mail em Conta.

---

## 📌 Prioridade sugerida

1. **Itens 1 e 2:** totais de 12 meses que não batem e projeção abaixo do histórico. São os números que o usuário compara.
2. **Item 4:** CSV de posições com "Proventos recebidos" zerado. O CSV é vendido como apoio ao imposto de renda.
3. **A, C e item 3:** layout e formatação. B é só um rótulo.
