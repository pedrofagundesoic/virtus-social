# Virtus: correções e novas funções (documento único)

Substitui `SUGESTOES-APP.md`, `-2`, `-3` e `-4` (rodadas de 24/09, 29/09, 07/10 e 13/10/2026; o texto completo de cada uma está no histórico do git).

**Última verificação:** 28/10/2026.
- **Web:** desktop 1440×900 e celular 390×844.
- **Android:** **v1.4.1** (Galaxy S25).
- **Conta de testes:** 15 ativos em 4 corretoras, compras de 2022–2023.
- **Fontes de conferência:** CSV exportado pelo próprio app, Yahoo Finance, Banco Central (séries 433, 4389 e 13522) e API da BRAPI.

**Como usar:**
1. **Seção 1:** o que falta corrigir.
2. **Seção 2:** nova função proposta (movimentação de administradores).
3. **Seções 3 e 4:** histórico, para não reabrir o que já foi resolvido ou descartado.

---

## 1. Em aberto

### 🔴 1.1 Preço justo, Snowflake e Safety score existem no Android, mas não no site (novo, 28/10)

**Onde:** no Android 1.4.1, o detalhe do ativo → aba **Fundamentos** tem:
- **Preço justo — 3 métodos** (Bazin, Graham e Gordon), com fórmula e margem;
- **Snowflake** (5 dimensões);
- **Comparação com pares**;
- **Safety score**.

No site, o detalhe do mesmo ativo (`/ativo/…`) mostra só P/L, P/VP, DY e ROE.

**Por que é prioritário:** a página de planos do site anuncia no Premium "**Preços justos pelos métodos de Bazin, Graham e Gordon**". Quem assina pelo site não encontra a função no site.

**Sugestão:** levar a aba Fundamentos inteira para a web, com o mesmo cálculo e as mesmas fontes do app, para os números baterem entre as plataformas.

### 🔴 1.2 Total de proventos caiu mais do que as duplicatas apontadas (novo, 28/10)

A deduplicação do item 1.1 da rodada anterior foi feita. O CSV não tem mais os pares duplicados, e as parcelas legítimas de PETR4 e KLBN11 continuam lá ✔. Mas a queda passou do que tinha sido identificado:

| | Antes (19/10) | Agora (28/10) | Diferença | Esperado pelas duplicatas apontadas |
|---|---|---|---|---|
| Total recebido (histórico) | R$ 25.043,61 | R$ 24.015,12 | **−R$ 1.028,49** | −R$ 639,55 (R$ 498,79 + R$ 140,76 inconclusivos de ITSA4) |
| ITSA4 (total do ativo) | R$ 2.690,59 | R$ 2.275,26 | −R$ 415,33 | −R$ 238,11 |
| PETR4 (total do ativo) | R$ 4.292,67 | R$ 3.962,47 | −R$ 330,20 | −R$ 103,02 |
| JCP bruto 2026 (Virtus IR) | R$ 1.272,84 | R$ 1.155,75 | −R$ 117,09 | −R$ 97,35 |

Além disso, entre 19/10 e 28/10 entraram pagamentos novos (BTLG11 e XPML11 em 23/10), o que deveria ter **aumentado** o total.

**Pergunta para o desenvolvedor:**
- Que outros registros de ITSA4 e PETR4 foram removidos além dos listados?
- Eles eram mesmo duplicados na fonte oficial?
- Exemplo: hoje PETR4 com data-com 27/04/2023 aparece **cinco** vezes no CSV, em 19/05, 16/06 (duas vezes cada) e 27/12/2023. Antes eram duas.

### 🟡 1.3 Ranking com DY fora da realidade (novo, 28/10)

Web → **Melhores Pagadoras**: o 8º colocado, **BVAR11**, aparece com "**DY 5a >999%**" e score 86. É um outlier de dado (provavelmente um evento de capital ou uma cotação errada). **Sugestão:** limitar o DY, por exemplo excluindo eventos acima de 100% ao ano da média de 5 anos, e não dar score a ativos com dado inconsistente.

### 🟡 1.4 Safety score: "Payout 13" ao lado de "payout implícito ≈ 100%" (novo, 28/10)

Android → BBSE3 → Safety score: o subtítulo diz "payout implícito ≈ 100%" e a barra de componente diz "Payout **13**". Para o usuário parece contradição. **Sugestão:** deixar claro na barra que 13 é a **nota** do componente (de 0 a 100) e que o payout medido é ≈ 100%. Por exemplo: "Payout (≈100%) · nota 13".

### ⚪ 1.5 Conferir (inconclusivo, para o desenvolvedor)

- **Comparação com pares (Android):**
  - todos os DY aparecem como números inteiros (16,00 · 14,00 · 11,00 · 10,00 · 9,00), o que sugere valor estimado ou arredondado;
  - BSLI3 aparece com P/L 1,72 e P/VP 0,30.
  - Vale conferir a fonte e a data desses números.
- **Graham (BBSE3):** o preço justo aparece como **R$ 24,44**.
  - Com VPA R$ 5,61 e o LPA implícito no P/L de 9,11 a R$ 41,57 (LPA ≈ 4,56), a fórmula √(22,5 × LPA × VPA) dá **≈ R$ 23,99**.
  - Diferença de ~2%, provavelmente porque o LPA vem de um período diferente do usado no P/L. Vale usar o mesmo LPA nos dois lugares.
  - Bazin (R$ 76,50) e Gordon (R$ 67,54) conferem com dividendos de 12 meses de ≈ R$ 4,59 por ação.
- **"Inspirado em Simply Wall St."** aparece na tela do Snowflake. É menção a marca de terceiro; vale avaliar com o jurídico.

### ⚪ 1.6 Não verificados desde 24/09

Ficam para quando houver tempo de testar o cadastro de ponta a ponta.

Doc 1:
- **#3:** cotação "—" logo após o cadastro.
- **#4:** campo de data que rejeita barras.
- **#5:** limite para percentuais fora da realidade.
- **#13:** a data volta para "hoje" a cada lançamento.
- **#14:** a tela recarrega inteira depois de salvar.

Doc 2:
- **#10:** data cortada em "Pagamentos recentes" no celular.

---

## 2. Nova função Premium: **Movimentação da diretoria** (insiders)

> Pedido do dono, 28/10/2026. Usa o novo endpoint da BRAPI Pro `GET /api/v2/stocks/insider-transactions` (dados oficiais da CVM desde 2018). Tudo o que está aqui foi testado na API real com PETR4, VALE3, MGLU3 e ITUB4, os tickers liberados sem token: 5.747 registros.

### 2.1 O que o usuário vê

Para cada ação, um selo que responde em uma linha: **"Nos últimos 6 meses, quem administra a empresa está comprando, vendendo ou parado? E isso é relevante?"**

| Selo | Quando |
|---|---|
| 🟢 **Diretoria comprando** · *relevante* / *forte* | compras líquidas, de forma consistente, e de tamanho relevante (ver 2.4) |
| 🔴 **Diretoria vendendo** · *relevante* / *forte* | vendas líquidas, de forma consistente, e de tamanho relevante |
| ⚪ **Estável** | há negociação, mas sem direção clara ou de tamanho pequeno |
| — **Sem negociações** | nenhuma compra ou venda em bolsa no período |
| ⏳ **Dados desatualizados** | o último relatório na CVM tem mais de 3 meses |

O selo aparece junto do **Preço justo (Bazin · Graham · Gordon)**, do **Safety score** e do **Snowflake**, formando um **painel de sinais** do ativo: preço, segurança do dividendo e comportamento de quem está dentro da empresa.

### 2.2 Como a API funciona (fatos medidos, que mudam o desenho)

1. **Relatório mensal, por empresa e por grupo de cargo, sem identificar a pessoa.**
   - Os registros vêm agrupados em `roleGroup`: `controller`, `board`, `director`, `statutoryBody`, `fiscalCouncil`.
   - **Não dá para contar "quantos diretores compraram".** A "abrangência" do sinal tem que ser medida em **meses** e **grupos de cargo** com a mesma direção.
2. **PETR3 e PETR4 retornam os mesmos dados**, porque o relatório é por CNPJ. É preciso guardar por empresa (CNPJ) e exibir em todos os tickers dela.
3. **`direction` (credit/debit) não é compra/venda.** Inclui posse, saída do cargo, bonificação, empréstimo etc. O sinal precisa de **`movementType`**. Tipos observados nos 4 tickers, de 5.747 registros:

   | Tratamento | `movementType` (contagem observada) |
   |---|---|
   | **Compra em bolsa (entra no sinal)** | Compra à vista (1.293) · Compra (27) · Compra à termo (3) |
   | **Venda em bolsa (entra no sinal)** | Venda à vista (2.724) · Venda (29) · Venda à termo (8) |
   | **Fora do sinal, mostrar como contexto** | Ações de plano de remuneração (86) · Homologação de subscrição (8) |
   | **Ignorar** | Posse (322) · Desligamento/saída (317) · Desdobramento/bonificação (269) · Outras Entradas (435) / Outras Saídas (57) · Contratação/Devolução de empréstimo (129) · Grupamento (18) · Doação (20) · Herança (2) · Ações reduzidas (2) |

   "Posse" e "Desligamento/saída" são o **saldo de quem entrou ou saiu do cargo**. Se fossem contados, uma troca de diretoria viraria um falso "comprando" ou "vendendo".
4. **Atraso de divulgação.** Da data do negócio (`transactionDate`) até a data de divulgação (`filingDate`), a mediana foi de **30 dias**, o percentil 90 de **231 dias** e o máximo de 1.646 dias (refilings).
   - Para não "ver o futuro", **a janela deve ser por `filingDate`**: só conta o que já era público.
   - A tela deve mostrar "Último relatório: set/2026 · divulgado em 13/10/2026".
5. **Versões.** A API devolve a última versão de cada relatório. Com `allVersions=true` vêm versões antigas, que **não podem ser somadas** (repetem movimentações). Guardar `id` + `version` e usar só a versão mais recente.
6. **Saldos iniciais não vêm na lista**, então não é possível saber a posição total do insider, só o fluxo.
7. **Limites:**
   - até 20 tickers por chamada e 100 registros por página;
   - o ITUB4 sozinho tem 3.395 registros (34 páginas) desde 2018;
   - a API respondeu **HTTP 429** com ~0,3 s entre chamadas; com 4 s entre páginas e espera crescente em caso de 429, funcionou.
   - **A carga inicial precisa ser lenta e incremental.**
8. **Atualização semanal** na BRAPI → job semanal (por exemplo, terça de madrugada) e incremental (`startDate` = última `filingDate` conhecida − 60 dias, por causa dos refilings).
9. **`companyRelation`:** usar `company`, ou seja, ações da própria empresa. Negociações em controladora ou controlada ficam fora do sinal.
10. **`securityType`:** usar só `Ações`. Ficam fora debêntures, opções e outros.

### 2.3 Cálculo (por empresa, janela padrão de 6 meses por `filingDate`; opções de 3 e 12 meses)

Dois grupos calculados **separadamente**:
- **Administração** = `board` + `director` + `statutoryBody` + `fiscalCouncil`. **É ela que define o selo.**
- **Controladores** = `controller`. Aparecem como contexto, porque venda de controlador costuma ser operação estrutural (oferta, venda de participação) e não "opinião" sobre o preço.

Para cada grupo:
```
compras  = Σ volume (movimentos de compra)        vendas = Σ volume (movimentos de venda)
saldo    = compras − vendas                        bruto  = compras + vendas
% compra = compras / bruto
meses_compra / meses_venda = nº de meses distintos (transactionDate) com compra / venda
intensidade_bps = |saldo| / valor_de_mercado × 10.000
intensidade_liquidez = |saldo| / volume_financeiro_médio_diário_3m
preço_médio_compra / preço_médio_venda = Σvolume / Σquantidade
```
Conferir `volume ≈ quantidade × preço unitário`; descartar a linha se divergir mais de 1%.

### 2.4 Regras do selo (padrões iniciais, recalibrar com o backtest da 2.7)

```
se não há relatório nos últimos 3 meses        → "Dados desatualizados"
se bruto == 0                                  → "Sem negociações"
direção = "comprando" se % compra ≥ 70% e saldo > 0 e meses_compra ≥ 2
          "vendendo"  se % compra ≤ 30% e saldo < 0 e meses_venda  ≥ 2
          senão "estável"
relevância (só se comprando/vendendo):
          "forte"      se intensidade_bps ≥ 5   ou intensidade_liquidez ≥ 100%
          "relevante"  se intensidade_bps ≥ 0,5 ou intensidade_liquidez ≥ 20%
          senão         → mostrar a direção com "pouco relevante" (cinza)
```
- **Venda pesa menos que compra.** Vendas acontecem por motivos pessoais: imposto, diversificação, vencimento de plano de remuneração. Por isso o texto do selo de venda é mais neutro, e a direção "vendendo" exige 3 meses, em vez de 2, para virar "relevante".
- **Detector de rotina:** se o mesmo grupo vendeu (ou comprou) no mesmo mês do ano em pelo menos 2 dos 3 anos anteriores, marcar "**padrão recorrente**" e rebaixar um nível. Isso segue a linha de Cohen, Malloy e Pomorski (2012), que separam negociações "rotineiras" das "oportunistas", e só as oportunistas tinham poder informativo. O caso típico é a venda mensal de bancos ligada a remuneração em ações (ver ITUB4 abaixo).
- **Os limites devem virar percentis:** depois do backtest, por exemplo, "relevante" = top 25% e "forte" = top 5% de `intensidade_bps` entre as empresas com negociação no período, recalculados todo mês.

**Casos de teste com dados reais** (janela 28/04 → 28/10/2026 por `filingDate`; valor de mercado da BRAPI em 28/10):

| Ticker | Grupo | Compras | Vendas | Saldo | % compra | Meses c/v | Intensidade | Selo esperado |
|---|---|---|---|---|---|---|---|---|
| PETR4 | Administração | R$ 254.340 | R$ 33.444 | +R$ 220.896 | 88% | 2 / 2 | 0,003 bp | 🟢 Comprando · *pouco relevante* |
| PETR4 | Controladores | 0 | R$ 8,97 bi | −R$ 8,97 bi | 0% | 0 / 3 | 124 bp | contexto: "Controlador vendeu R$ 8,97 bi" |
| VALE3 | Administração | R$ 1.107.336 | R$ 20.380 | +R$ 1.086.956 | 98% | 4 / 1 | 0,04 bp | 🟢 Comprando · *pouco relevante* |
| ITUB4 | Administração | R$ 147.944 | R$ 80,8 mi | −R$ 80,7 mi | 0% | 1 / 6 | 1,7 bp | 🔴 Vendendo · relevante → **padrão recorrente** (rebaixa) |
| MGLU3 | Administração | 0 | 0 | 0 | — | 0 / 0 | — | — Sem negociações |
| MGLU3 | Controladores | 0 | R$ 30,9 mi | −R$ 30,9 mi | 0% | 0 / 2 | 76 bp | contexto: "Controladores venderam R$ 30,9 mi" |

Esses números saem da API como ela respondeu em 28/10/2026 e podem mudar com refilings. Servem para conferir a implementação.

### 2.5 Telas

**App (Android/iOS) e site, no detalhe do ativo → aba Fundamentos**, card "**Movimentação da diretoria**", logo abaixo de "Preço justo":
1. Selo grande (2.1) + frase gerada: "Nos últimos 6 meses, a administração comprou R$ 1,1 mi e vendeu R$ 20 mil em ações da empresa, em 4 meses diferentes."
2. **Gráfico de barras mensal (12 meses)**: compras para cima (verde), vendas para baixo (vermelho), com a linha do preço da ação por cima.
3. Números: compras, vendas, saldo, % do valor de mercado e preço médio pago pela administração × cotação atual ("a administração comprou a R$ X em média; hoje R$ Y").
4. Alternar **Administração | Controladores | Todos** e **3m | 6m | 12m**.
5. Lista das últimas negociações: mês, grupo de cargo, compra/venda, quantidade, preço e corretora. A pessoa não é identificada, como na fonte.
6. Linha de contexto, fora do selo: "Plano de remuneração: X ações recebidas" quando houver.
7. Rodapé: "Último relatório: set/2026 · divulgado à CVM em 13/10/2026 · Fonte: CVM via BRAPI."
8. (i) **Como calculamos**: os tipos que contam, a janela por data de divulgação, os limites de relevância, o detector de rotina e o resultado do backtest (2.7). É o mesmo padrão do "como calculamos" dos Prováveis Pagadores.

**Outros pontos do app:**
- **Carteira e Watchlist:** um chip pequeno no card do ativo **só quando o selo é relevante ou forte** ("🟢 Diretoria comprando"). Sem chip nos demais casos, para não poluir.
- **Notificação (Premium):** "A administração da BBSE3 passou a comprar de forma relevante" quando o selo de um ativo da carteira ou da Watchlist **muda** para relevante ou forte. No máximo uma por ativo por mês.
- **Nova tela "Radar de insiders"** (em Análises → Análises premium, e no menu Premium do site): ranking das empresas por `intensidade_bps` de compra líquida da administração nos últimos 6 meses. Filtros: setor, só minha carteira ou Watchlist, comprando ou vendendo, relevância. Botão para ver o card do ativo.
- **Usuário grátis:** o card aparece borrado com "Disponível no Premium", igual às outras funções Premium.

**Site e lojas (divulgação):**
- Na lista do plano Premium da página inicial, acrescentar: "**Movimentação da diretoria: veja se quem administra a empresa está comprando ou vendendo as próprias ações (dados da CVM)**".
- Acrescentar o mesmo item na descrição da App Store e da Google Play e na tela de assinatura do app.
- Ao lançar, aproveitar para garantir o item 1.1: as funções de preço justo também precisam estar no site.

### 2.6 Backend

- **Tabelas:**
  - `insider_transactions`: `id` (PK, o id da BRAPI), `cnpj`, `report_date`, `filing_date`, `version`, `transaction_date`, `company_relation`, `role_group`, `direction`, `movement_type`, `security_type`, `security_class`, `quantity`, `unit_price`, `volume`, `intermediary`, `fetched_at`.
  - `insider_signal`: `cnpj`, `as_of`, `janela`, `grupo`, métricas da 2.3, `direcao`, `relevancia`, `recorrente`, `ultimo_relatorio`, `ultima_divulgacao`.
- **Universo:**
  - primeiro, empresas presentes em alguma carteira ou Watchlist;
  - depois, o Ibovespa;
  - depois, o universo do Ranking.
  - Deduplicar por CNPJ, com uma chamada por empresa, mesmo com dois tickers.
- **Jobs:**
  - **Carga inicial:** 2018→hoje, lenta, com espera crescente quando vier 429, retomável.
  - **Semanal incremental:** últimos 60 dias de `filingDate`.
  - **Recalcular `insider_signal`** depois de cada carga.
- **API interna:** `GET /api/insiders/:ticker?janela=6m&grupo=adm` → selo, métricas, série mensal e últimas 20 negociações. Cache de 24 h.
- **Valor de mercado e liquidez:** usar o que o app já busca na BRAPI (`marketCap`) e o volume diário do histórico de preços.
- **Ponto no tempo:** todo cálculo aceita `as_of` e usa só registros com `filing_date ≤ as_of`. Isso é obrigatório para o backtest e para o histórico do selo.

### 2.7 Validação antes de divulgar como "sinal" (importante)

- **O que diz a literatura:** compras de insiders tendem a anteceder retornos acima do mercado, com efeito maior em empresas pequenas e em compras concentradas. Vendas têm pouco poder informativo. Referências: Seyhun (1986); Lakonishok e Lee (2001); Cohen, Malloy e Pomorski (2012).
- **O que deu nos nossos dados, num teste rápido** com os 4 tickers grandes liberados (retorno da ação 3 meses depois de um mês com compra líquida da administração, comparado com a média de todos os meses):

  | Ticker | Após compra líquida | Após venda líquida | Todos os meses | n (compra / venda) |
  |---|---|---|---|---|
  | PETR4 | +10,3% | +6,7% | +8,0% | 44 / 17 |
  | VALE3 | +5,9% | +2,0% | +5,5% | 51 / 15 |
  | MGLU3 | +14,4% | +6,4% | 0,0% | 6 / 12 |
  | ITUB4 | 0,0% | +3,0% | +3,5% | 4 / 73 |

  Em empresas grandes o efeito foi **pequeno e inconsistente**, e a amostra é pequena demais para concluir. Isso combina com a literatura: em empresas muito acompanhadas por analistas, o sinal é fraco.

**Recomendação:**
- Lançar a função como **informação de contexto**, não como sinal de compra.
- Antes de qualquer texto do tipo "historicamente, empresas com compras relevantes da diretoria…", rodar o backtest completo, com todas as empresas, de 2019 a 2026:
  - janela por `filingDate`, sem olhar o futuro;
  - retorno em excesso ao Ibovespa em 3, 6 e 12 meses;
  - quebras por tamanho (terços de valor de mercado), por relevância e por rotina × oportunista;
  - publicar o resultado em "Como calculamos", como já é feito com os 95% de acerto dos Prováveis Pagadores.
- **Não usar no app os números e exemplos do texto do Gemini** ("5% a 10% ao ano", "3,5% em 3 meses", GOAU4/2015, HBOR3/2016). Não há fonte verificável para eles. Se forem usados, precisam de referência conferida.

### 2.8 Textos e conformidade

- **Linguagem neutra e descritiva:** "a administração comprou mais do que vendeu", e não "momento de compra". Selos sem verbo de ação para o usuário.
- **Aviso fixo no card:** "Informação pública divulgada à CVM (Resolução CVM 44/2021, art. 11). Negociações de administradores podem ter motivos pessoais e não indicam, por si só, a direção do preço. Não é recomendação de investimento."
- **Não identificar pessoas**, mesmo que algum dia a fonte passe a permitir. Mostrar só o grupo de cargo.

### 2.9 Critérios de aceite

1. Os casos da tabela da 2.4 produzem os selos esperados.
2. PETR3 e PETR4 mostram o mesmo card.
3. "Posse", "Desligamento/saída", bonificação, empréstimo e plano de remuneração **não** alteram compras, vendas nem saldo.
4. Com `allVersions=true` na carga, o saldo não muda (só a última versão conta).
5. Com `as_of` = 01/06/2026, nenhum registro com `filingDate` posterior entra no cálculo.
6. Usuário grátis vê o card borrado; Premium vê tudo, no app e no site.
7. O card aparece no site e no app com números idênticos.
8. A carga semanal termina sem erro 429 não tratado e é retomável.

---

## 3. Resolvido (para não reabrir)

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
| Gráfico de 12 meses com degrau / "411% do CDI" | 13/10 | Curva contínua (bate com as cotações reais) |
| YoC da carteira 0,06% | 13/10 | ≈ 9,8% |
| Virtus IR com dividendos zerados | 13/10 → 19/10 | Iguais ao CSV |
| "Recebido últimos 12M" R$ 36,95 / proventos do mês R$ 0,00 | 13/10 | Corretos |
| Fluxo de renda cortado no celular / rótulos sobrepostos | 13/10 | Lista no celular, sem sobreposição |
| Calendário do Android cortando valores | 13/10 | Valores completos |
| Três totais de 12 meses diferentes | 19/10 | Janela de 365 dias em todo lugar; o calendário diz a janela |
| Projeção 12M abaixo do histórico | 19/10 | Fórmula explicada na tela |
| CSV de posições sem proventos / com abreviações | 19/10 | Preenchido; nomes completos |
| Ponto decimal e data ISO no Android | 19/10 | Vírgula e dd/mm/aaaa |
| Patrimônio vazando do card (web, celular) | 19/10 | Cabe |
| E-mail no rodapé da barra lateral (web) | 19/10 | Só "Plano Premium" |
| Rótulo do IPCA no período "Mês" | 19/10 | "IPCA set/26" |
| "Prováveis Pagadores" com 80 mil px no celular | 13/10 | Filtro "Só minha carteira" |
| Proventos em dobro (mesmo provento duas vezes / registro provisório mantido) | 28/10 | Pares removidos; parcelas de PETR4 e KLBN11 preservadas (ver 1.2 sobre a queda maior que a esperada) |
| Botão "+" cobrindo a busca (Android) | 28/10 | Não cobre mais |
| BTLG11 sem corretora / "NUINV" nos filtros (Android) | 28/10 | "Fundos Imobiliários · NuInvest"; filtros "BTG Pactual", "Inter"… |
| Ponto decimal em P/L e P/VP (web) | 28/10 | "9,11" e "7,69" |
| Duas médias no mesmo gráfico (web) | 28/10 | "média R$ 486,82/mês" na linha e na legenda |

## 4. Conferido e descartado (não era erro)

| Suspeita | Por que não era erro |
|---|---|
| Período "Mês" com IBOV +9,99% e carteira +7% (07/10) | Ibovespa real +9,66% na semana; carteira recalculada com cotações reais: +6,96% |
| IPCA +0,82% no mês (13/10) | É o IPCA de set/2026 divulgado pelo IBGE (0,82%, série 433 do BCB) |
| Gráfico do mês com salto no início (13/10) | O Ibovespa subiu 7,7% num único dia (05/10) |
| "Contexto macro": IPCA 12m 4,58%, CDI 13,65% (19/10) | Conferem com as séries 13522 e 4389 do BCB |
| PETR4 e KLBN11 com o mesmo provento pago 2–3 vezes (19/10) | São parcelas de um mesmo evento |
| Preço justo Bazin R$ 76,50 e Gordon R$ 67,54 (BBSE3, 28/10) | Batem com dividendos de 12 meses de ≈ R$ 4,59 por ação: 4,59 ÷ 6% e 4,59 × 1,03 ÷ (10% − 3%) |
