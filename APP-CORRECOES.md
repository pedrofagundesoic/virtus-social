# Virtus: correções e novas funções (documento único)

Substitui `SUGESTOES-APP.md`, `-2`, `-3` e `-4` (rodadas de 24/09, 29/09, 07/10 e 13/10/2026; o texto completo de cada uma está no histórico do git).

**Última verificação:** 09/11/2026.
- **Web:** desktop 1440×900 e celular 390×844.
- **Android:** **v1.5.1** (Galaxy S25).
- **Conta de testes:** 15 ativos em 4 corretoras, compras de 2022–2023.
- **Fontes de conferência:** CSV exportado pelo próprio app, Yahoo Finance, Banco Central, API da BRAPI e texto consolidado da Resolução CVM 20.

**Como usar:**
1. **Seção 1:** o que falta corrigir.
2. **Seção 2:** nova função proposta (movimentação de administradores).
3. **Seções 3 e 4:** histórico, para não reabrir o que já foi resolvido ou descartado.

---

## 1. Em aberto

### 🔴 1.1 Titãs da Renda: página teórica e educacional, sem texto por empresa até o advogado opinar

**Decisão do dono:** o Virtus não tem CNPI nem analista contratado, então não há quem assine. A página deve deixar claro que é uma carteira teórica e educacional, e ganhar um FAQ, como em meusdividendos.com/carteiras.

**Atenção antes de publicar:** só o aviso não resolve o ponto levantado.
- O art. 1º, §1º da Resolução CVM 20 chama de relatório de análise "quaisquer textos, relatórios de acompanhamento, estudos ou análises sobre valores mobiliários específicos ou sobre emissores de valores mobiliários determinados que possam auxiliar ou influenciar investidores". Não exige recomendação, e não encontrei na norma exceção para conteúdo "teórico" ou "educacional".
- O art. 2º torna a atividade privativa de credenciados. Por isso a alternativa indicada na mensagem do desenvolvedor (tirar os textos por empresa) é a mais segura.
- **A página de referência é diferente da nossa:** a Meus Dividendos mostra um backtest por regra (top 10 de cada tese, peso igual, rebalanceamento mensal), com posições e números. Na parte que li não há texto próprio por empresa. Os Titãs têm "Por que está na lista", "Perfil de renda" e "Principais riscos" para cada uma das 13 empresas, que é justamente o que se encaixa na definição.

**Implementação sugerida:**
1. **Tirar da página, por enquanto, os textos por empresa** (Por que está na lista, Perfil de renda, Principais riscos).
2. **Manter a parte por regra:** setores, composição gerada pelo método VRE, notas e números.
3. **Publicar a metodologia:** critérios, frequência de atualização e, se possível, um backtest com custos declarados.
4. **Levar ao advogado** duas perguntas: uma lista teórica por regra, com nomes de empresas e sem texto, fica fora do art. 1º, §1º? E se a resposta permitir, em que condições os textos poderiam voltar?

**Texto para o topo da página** (escrito pelo Virtus; hoje o aviso é idêntico ao da Meus Dividendos):

> **Carteira teórica, com finalidade educacional.** Os Titãs da Renda são uma simulação gerada automaticamente pelo método VRE, com apoio de inteligência artificial, a partir de dados públicos. A seleção busca, em teoria, empresas de setores perenes com histórico consistente de proventos.
>
> Não é recomendação de compra, venda ou manutenção, não considera o seu perfil ou objetivos e não foi elaborada por analista de valores mobiliários. Rentabilidade e proventos passados não garantem resultados futuros. As decisões de investimento são de responsabilidade de cada investidor.

*Observação:* evitei "poderia ter um melhor retorno", porque soa como promessa. Se a frase do apoio de IA for mantida, ela só informa a origem do conteúdo; não muda o enquadramento.

**FAQ para o fim da página:**

- **O que são os Titãs da Renda?** Uma carteira teórica, gerada por regras a partir de dados públicos, para estudar empresas de setores perenes com histórico de proventos.
- **Isso é uma recomendação de investimento?** Não. A carteira não indica compra, venda ou manutenção de nenhum ativo.
- **Posso copiar essa carteira?** Ela não foi feita para ser copiada. Não considera o seu perfil, patrimônio, prazo ou momento de entrada.
- **Como as empresas são escolhidas?** Pelo método VRE. *(Inserir os critérios e pesos reais.)*
- **Com que frequência ela muda?** *(Inserir a frequência real.)*
- **Qual é o papel da inteligência artificial?** *(Descrever o que ela faz de fato.)*
- **Um analista revisa o conteúdo?** Não. O conteúdo é gerado automaticamente e não passa por analista de valores mobiliários.
- **Os resultados são garantidos?** Não. Rentabilidade e proventos passados não garantem resultados futuros.
- **A carteira considera custos e impostos?** *(Responder conforme o cálculo real.)*

**Conferir também:** o selo "Premium" e os textos de venda não devem apresentar os Titãs como indicação de ativos. O mesmo texto e o FAQ valem para o site e o app.

### 🔴 1.2 Instagram: post de 05/11 saiu só no Facebook (publicador, sem ação do desenvolvedor do app)

O post "De olho antes de comprar" recebeu "Media ID is not available" ao publicar no Instagram. O Instagram estava processando a imagem e o script publicou mesmo sem confirmação de que estava pronta. Correção de nossa parte, no publicador do social.

### 🟡 1.3 Site no celular: "Passe o mouse para ver cada dia"

Continua em Carteira → Visão geral. **Sugestão:** "Toque no gráfico para ver cada dia".

### 🟡 1.4 Movimentação da diretoria: "em 1 mês diferente"

PETR4 (Android): "comprou R$ 206,1 mil e vendeu R$ 13,5 mil em ações da empresa, em 1 mês diferente." **Sugestão:** no singular, "em 1 mês".

### 🟡 1.5 Top 5 (Android): ticker repetido

"MXRF11 / MXRF11" e "TAEE11 / TAEE11": quando não há nome da empresa, a segunda linha repete o ticker. **Sugestão:** usar o nome curto ou esconder a linha.

### 🟡 1.6 Calendário como função do plano grátis? (ideia, 09/11)

O público de dividendos quer saber quando as empresas pagam, e o Mapa de Dividendos é só Premium. **Sugestão a avaliar:** mostrar no plano grátis as 5 primeiras linhas, ou apenas o mês atual, com o restante borrado.

### ⚪ 1.7 Para o desenvolvedor conferir (inconclusivo)

- **Dietz × TWR (Android, Análises → Métricas de carteira):** "TWR 13,88%" e "Dietz 45,83%", na mesma janela de 365 dias. Sem aportes no período, os dois deveriam ficar próximos. Os lançamentos da conta são de 2022–2023, então parece que o Dietz está usando outra janela.
- **Site em telas de 320 px:** o seletor "Ibovespa | CDI" sai da tela e a barra inferior fica parcialmente fora da área visível (visto em simulação; em 360 e 390 px está certo).

### ⚪ 1.8 Da especificação da Movimentação da diretoria, ainda não testados

Assinante vê tudo, mas não testei com conta grátis (card borrado). Também não testei: notificação de mudança de selo, chip na Carteira e na Watchlist, PETR3 × PETR4 com o mesmo card, detector de rotina em ITUB4, textos nas lojas e o backtest da seção 2.7.

### ⚪ 1.9 Não verificados desde 24/09

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

## 2. Função Premium: **Movimentação da diretoria** (insiders)

**Situação em 04/11:** implementada no site e no Android 1.5.0, com card no ativo, Radar de insiders e item na página de planos. Os selos de PETR4 conferem com a tabela da 2.4 ("comprando · pouco relevante", R$ 254,3 mil × R$ 33,4 mil, 0,003 bp, controlador vendeu R$ 9 bi). Falta o que está em 1.8. A especificação fica aqui como referência.

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
| Preço justo, Snowflake, Safety score e pares só no Android | 04/11 | Agora também no detalhe do ativo no site |
| Queda de proventos maior que as duplicatas | 04/11 | Conferido com a Yahoo: ITSA4 R$ 2.161,91 × R$ 2.159,30. TAEE11 difere R$ 90,03, exatamente os dois pagamentos de 26/11 ainda não recebidos |
| BVAR11 com "DY 5a >999%" no Ranking | 04/11 | Saiu da lista |
| Safety score "Payout 13" × "payout ≈ 100%" | 04/11 | "Payout ≈96% · nota 18", com legenda explicando as barras |
| Comparação com pares com DY inteiro | 04/11 | DY com decimais (ex.: 29,54 · 23,88) |
| LPA do Graham diferente do P/L | 04/11 | Mesmo LPA nos dois (R$ 4,73), com a data do balanço na tela |
| "Inspirado em Simply Wall St." no Snowflake | 04/11 | Removido |
| "Carteira Recomendada" trocado por "Titãs da Renda" | 09/11 | Site e app; endereço antigo redireciona; "peso sugerido", "Tese" e "Encaixe" renomeados |
| P/VP diferente do VPA do Graham | 09/11 | 5,54 = cotação ÷ VPA R$ 6,94 |
| Botão "Todos" quebrado (Android) | 09/11 | Em uma linha |
| "Adicionar" cobrindo o gráfico (Android) | 09/11 | Foi para o topo da tela |
| Radar: "bp" e nome longo da Klabin | 09/11 | "2,13% do valor de mercado"; "Klabin SA" |

## 4. Conferido e descartado (não era erro)

| Suspeita | Por que não era erro |
|---|---|
| Período "Mês" com IBOV +9,99% e carteira +7% (07/10) | Ibovespa real +9,66% na semana; carteira recalculada com cotações reais: +6,96% |
| IPCA +0,82% no mês (13/10) | É o IPCA de set/2026 divulgado pelo IBGE (0,82%, série 433 do BCB) |
| Gráfico do mês com salto no início (13/10) | O Ibovespa subiu 7,7% num único dia (05/10) |
| "Contexto macro": IPCA 12m 4,58%, CDI 13,65% (19/10) | Conferem com as séries 13522 e 4389 do BCB |
| PETR4 e KLBN11 com o mesmo provento pago 2–3 vezes (19/10) | São parcelas de um mesmo evento |
| Preço justo Bazin R$ 76,50 e Gordon R$ 67,54 (BBSE3, 28/10) | Batem com dividendos de 12 meses de ≈ R$ 4,59 por ação: 4,59 ÷ 6% e 4,59 × 1,03 ÷ (10% − 3%) |
| "Sem negociações" em BBSE3 com vendas na lista (04/11) | As vendas são de mar/2026 ou antes, fora da janela de 6 meses por data de divulgação |
| Proventos R$ 0,00 no período "Mês" (Android, 09/11) | Em novembro ainda não houve pagamento nessa carteira; os primeiros são em 12 e 16/11 |
