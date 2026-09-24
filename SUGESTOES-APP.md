# Virtus — sugestões de aprimoramento do app

**Contexto:** observações feitas em 24/09/2026 no app Android **v1.3.4**, Galaxy S25 (Android, tela 1080×2340), conta de testes `pedrocfagundes@gmail.com` (27 ativos na Carteira Principal, 1 na Watchlist). Navegação feita tela a tela, incluindo cadastro de um ativo novo do zero.

Ordenado por impacto. Cada item traz o que acontece, como reproduzir e a sugestão.

---

## 🔴 Bugs / comportamentos que atrapalham

### 1. O lançamento ignora a carteira selecionada e vai sempre para a carteira padrão

**O que acontece:** criei a sub-carteira "Renda Passiva", deixei ela selecionada no seletor do topo e cadastrei ITSA4 pelo botão "Adicionar". O ativo foi salvo na **Carteira Principal**. A "Renda Passiva" continuou com `R$ 0,00` e `0 posições`.

**Como reproduzir:**
1. Carteira → seletor do topo → "Nova carteira" → criar "Renda Passiva" (fica selecionada)
2. Botão "+ Adicionar" → preencher qualquer ativo → "Salvar aplicação"
3. O ativo aparece em "Carteira Principal", não em "Renda Passiva"

**Sugestão:** o formulário "Nova aplicação" deve ter um campo **Carteira**, pré-selecionado com a carteira ativa no momento em que o formulário foi aberto (e com a padrão quando a seleção for "Todas as carteiras"). Hoje não há nenhuma indicação, no formulário, de onde o lançamento vai cair — o usuário só descobre depois de salvar.

---

### 2. Não há como gerenciar as carteiras depois de criadas

**O que acontece:** o sheet "Carteiras" só lista e seleciona. Não encontrei como **definir outra carteira como padrão**, **renomear**, **excluir** ou **mover ativos entre carteiras**. Long-press no item apenas seleciona. Não há nada sobre carteiras em Conta/Configurações.

**Impacto:** combinado com o item 1, uma sub-carteira criada por engano fica inútil e sem como remover, e não há como corrigir um lançamento que caiu na carteira errada.

**Sugestão:** menu de contexto (long-press ou ícone `⋮`) em cada carteira com: *Renomear*, *Definir como padrão*, *Excluir* (com aviso do que acontece com os lançamentos) e, no detalhe do ativo, *Mover para outra carteira*.

---

### 3. "Cotação atual" e "Valor de mercado" ficam em `—` por cerca de uma hora depois do cadastro

**O que acontece:** no detalhe do ITSA4 recém-lançado, os campos ficaram assim por ~40 minutos, através de várias reentradas na tela (depois disso passaram a mostrar R$ 14,24 normalmente — ou seja, não é dado ausente, é atraso de atualização):

```
Valor aplicado      R$ 3.680,00
Cotação atual       —
Valor de mercado    —
Proventos (total)   R$ 951,34
Proventos 12m       R$ 457,24
Yield on cost (12m) +12,43%
```

No **mesmo card**, logo abaixo, os "Indicadores fundamentalistas" do mesmo ativo carregaram normalmente (P/L 8.87 · P/VPA 1.72 · VPA R$ 8,36 · DY 8,00% · ROE 19,36% · Market Cap R$ 161,25 bi · *Fonte: BRAPI · atualizado 2026-09-24T03:55:42Z*). Ou seja: a cotação existe na fonte, mas não chegou nesses dois campos.

**Sugestão:** buscar a cotação do ativo assim que a primeira ordem dele é salva, em vez de esperar o próximo ciclo de atualização em lote. Enquanto não houver valor, usar *skeleton* de carregamento em vez de `—`. Um `—` silencioso parece dado faltando no cadastro do usuário, não atualização pendente — e é logo depois do primeiro cadastro que o usuário está mais inseguro sobre ter feito certo.

---

### 4. Campo de data rejeita separadores digitados

**O que acontece:** no seletor de data, ao alternar para entrada por texto (ícone de lápis) e digitar `12/03/2024`, o campo fica com `12/03/` — a máscara insere as barras automaticamente e não ignora as que o usuário digitou, comendo o ano. Só funciona digitando `12032024`.

**Sugestão:** o formatter deve descartar não-dígitos da entrada antes de aplicar a máscara. É o caminho natural de quem cola uma data ou digita como está acostumado — e o erro é silencioso: o campo simplesmente fica incompleto.

---

### 5. Percentuais de rentabilidade sem tratamento de outlier

**O que acontece:** a conta de testes mostra números que destroem a credibilidade da tela:

| Onde | Valor exibido |
|---|---|
| Card de patrimônio | `+298,48%` |
| Rentabilidade · 12 meses | `+7684,96%` e **`53000% do CDI`** |
| Posição BRCO11 | `+999,4%` |
| Posição HGLG11 | `+1373,4%` |
| Posição HGRE11 | `+1042,9%` |

A causa nesses casos é preço médio irreal (vários FIIs com PM `R$ 10,00`), mas o efeito vale para qualquer usuário que erre um lançamento ou tenha período curto demais: o indicador deixa de informar e passa a parecer defeito.

**Sugestão:**
- limitar a exibição (ex.: acima de `+999%` mostrar `>999%`);
- para "% do CDI", exigir um período mínimo e não exibir o indicador quando a série for curta demais — exibir `n/d` com um tooltip explicando;
- opcionalmente, sinalizar no card da posição quando o preço médio parecer inconsistente com o histórico de cotação do ativo ("confira seus lançamentos").

---

### 6. O botão flutuante "Adicionar" cobre conteúdo dos cards

**O que acontece:** na lista de posições, o FAB verde fica sobre o card imediatamente abaixo e esconde os campos "Preço médio"/"Cotação". Acontece em toda rolagem, inclusive no fim da lista.

**Sugestão:** `padding-bottom` na lista equivalente à altura do FAB + margem (~96 dp), para que o último card role acima dele.

---

### 7. "Editar ordens" está escondido atrás de um botão chamado "Adicionar movimentação"

**O que acontece:** a funcionalidade existe e funciona bem, mas é impossível de descobrir sozinho. O caminho é:

`Carteira → toca no ativo → **Adicionar movimentação** → Editar ordens → toca na ordem → Excluir ordem → Excluir`

Ou seja: para **ver, corrigir ou apagar** o que já existe, é preciso clicar em um botão que diz **adicionar**. Explorando o detalhe do ativo de cima a baixo (a tela termina nos "Indicadores fundamentalistas"), não há nenhum outro sinal de que os lançamentos podem ser listados ou editados — eu só encontrei o caminho depois de alguém me explicar.

**Sugestão:**
- renomear o botão para algo neutro, como **"Movimentações"**, e deixar o menu com *Novo aporte · Resgate · Editar ordens*; ou
- mostrar a lista de ordens direto no detalhe do ativo (seção "Movimentações", com data, tipo, quantidade, preço e corretora), com editar/excluir por item.

O diálogo de confirmação ("A ordem será removida permanentemente e a posição do ativo será recalculada") e o recálculo automático estão ótimos — o problema é só chegar até lá.

**Observação relacionada:** editar a ordem é justamente o caminho para corrigir os preços médios de `R$ 10,00` do item 5 — vale ter isso à mão no suporte.

---

## 🟡 Melhorias de usabilidade

### 8. Busca e ordenação na lista de posições

Com 27 ativos, achar um exige rolar muito, e a ordem parece ser só alfabética. Sugestão: campo de busca no topo e ordenação por **valor de mercado**, **rentabilidade**, **proventos recebidos** e **classe**, além de agrupar por classe (Ações BR, FIIs, BDRs, ETFs) com subtotal por grupo.

### 9. O texto da legenda do Mapa de Dividendos contradiz a escala

A tela diz *"Mais escuro = mais frequente"*, mas a legenda vai de `Não paga` (vazio) → `Eventual` (verde escuro) → `Frequente` (verde médio) → `Quase sempre` (verde claro/vivo). Visualmente o **mais claro** é o mais frequente. Sugestão: trocar o texto para "mais vivo = mais frequente" ou inverter a rampa de cor.

### 10. Afirmação de acerto sem link para metodologia

Em "Prováveis Pagadores": *"✓ 95% de acerto nas previsões dos últimos 12 meses (backtest + publicados)"*. É uma afirmação forte e verificável — vale um link "como calculamos" abrindo a metodologia (janela considerada, o que conta como acerto, o que é backtest vs. publicado). Protege o app de questionamento e aumenta a confiança.

### 11. Watchlist: card de resumo grande demais para poucos itens

Com 1 ativo monitorado, o cabeçalho ("Watchlist" + explicação + "1 ativo monitorado") ocupa cerca de um terço da tela e sobra uma área vazia enorme. Sugestão: compactar o cabeçalho quando houver poucos itens, ou usar o espaço vazio para sugerir ativos a acompanhar.

### 12. Primeiro chip da lista de corretoras aparece cortado

Em "Onde está esse ativo?", a lista horizontal de corretoras começa já rolada: o primeiro chip aparece cortado na borda esquerda. Sugestão: `contentPadding` inicial e garantir que a lista comece na posição 0.

### 13. Data da operação sempre volta para "Hoje"

Quem está cadastrando o histórico lança vários ativos com datas antigas seguidas. Sugestão: lembrar a última data usada na sessão como valor inicial do próximo lançamento.

### 14. Recarregamento completo após salvar

Ao salvar uma aplicação, a tela de carteira volta e exibe skeleton de vários segundos recarregando tudo. Sugestão: inserir a posição nova localmente e atualizar só o que mudou.

### 15. Exportar dados

Exportar carteira, lançamentos e proventos em CSV/Excel — útil para imposto de renda e para quem quer conferir a conta fora do app.

---

## 📌 Resumo em uma linha por item

| # | Item | Tipo |
|---|---|---|
| 1 | Lançamento ignora a carteira selecionada | 🔴 Bug |
| 2 | Carteiras não podem ser renomeadas, excluídas nem definidas como padrão | 🔴 Bug |
| 3 | "Cotação atual"/"Valor de mercado" em `—` por ~1h depois do cadastro | 🔴 Bug |
| 4 | Campo de data rejeita separadores digitados | 🔴 Bug |
| 5 | Percentuais de rentabilidade sem limite de outlier (`53000% do CDI`) | 🔴 Bug |
| 6 | FAB "Adicionar" cobre conteúdo dos cards | 🔴 Bug |
| 7 | "Editar ordens" escondido atrás do botão "Adicionar movimentação" | 🟡 UX |
| 8 | Busca, ordenação e agrupamento na lista de posições | 🟡 UX |
| 9 | Legenda do Mapa de Dividendos contradiz a escala de cor | 🟡 UX |
| 10 | "95% de acerto" sem link para metodologia | 🟡 UX |
| 11 | Cabeçalho da Watchlist grande demais para poucos itens | 🟡 UX |
| 12 | Primeiro chip de corretora cortado | 🟡 UX |
| 13 | Data da operação sempre volta para hoje | 🟡 UX |
| 14 | Recarregamento completo após salvar | 🟡 UX |
| 15 | Exportar dados em CSV | 🟡 UX |

---

## ✅ O que está muito bom (para não mexer sem querer)

- **Mapa de Dividendos** — o heatmap mês a mês com o DY na lateral é o tipo de coisa que não existe em app concorrente; leitura instantânea.
- **Melhores Pagadoras** — "30 anos de proventos · desde o Plano Real · 716 ativos ranqueados", com pódio e score 0–100, é forte e a fonte (B3/BRAPI + IPCA/BCB) está declarada na tela.
- **Próximos pagamentos** — trazer data ex, data de pagamento, valor por cota **e** a estimativa pela posição atual em um único bloco resolve exatamente a dor de quem vive de proventos.
- **Yield on cost (12m)** no detalhe do ativo, junto de proventos totais e 12m — indicador certo, no lugar certo.
- **"Toque para registrar compra"** no item da Watchlist — atalho ótimo, transforma acompanhamento em lançamento sem fricção.
- O aviso de que os valores têm caráter informativo e não são recomendação aparece no lugar certo, na tela de Conta.
