# Qualidade dos posts — falhas conhecidas e como evitar

Registro de problemas que passaram para posts publicados. Ler antes de montar um lote.

## 2026-10-10 · `2026-10-10-pagadores-do-mes` — mancha em volta do dedo

**O que aconteceu:** foto `voRfgeyiBKA` (polegar sobre a tela do iPhone). O `photo-screen.py` com `occlude: true`
devolveu à imagem os pixels da foto que "não pareciam tela" — além do polegar, a **sombra do polegar sobre a tela
branca original** (cinza, pouco saturada, brilho médio). Resultado: uma mancha cinza borrada em volta da ponta do
dedo, apagando parte do card "BBDC4". Ajustar `screen_sat`/`screen_v` só diminuiu a mancha. O dono aprovou mesmo
assim (prioridade: volume), mas pediu registro.

**Causa:** a máscara de oclusão é uma heurística de cor (HSV). Sombra de dedo, reflexo e pele clara ficam na
fronteira entre "tela" e "objeto na frente" — não há limiar que separe bem.

**Regras daqui em diante:**
1. **Preferir fotos sem nada na frente da tela** (dedos só nas bordas do aparelho). É o caso mais comum e não precisa de `occlude`.
2. Se usar `occlude`, revisar a área do dedo **com zoom 100%** (recorte da região, não a miniatura) antes de mostrar ao dono, e citar o ponto na aprovação.
3. Mancha visível = trocar a foto. Não tentar "consertar" com limiar.
4. Melhoria futura possível: máscara de oclusão desenhada à mão (polígono do dedo em `screens.json`) em vez de heurística de cor.

## 2026-10-14 · `2026-10-14-historico-por-ativo` — print menor que a tela, faixa preta e dedo fantasma

**O que aconteceu:** foto `p0Sn8X2htRs` (dois polegares, iPhone inclinado). Três defeitos ao mesmo tempo:
1. **Quad pequeno demais**: sobrou a tela branca original na lateral esquerda e na base (cantos medidos no olho, em grade de 100 px).
2. **Faixa preta no topo**: `status_bar: 70` pintou uma barra preta que não existe no aparelho real; ficou parecendo defeito.
3. **Dedo fantasma**: `occlude` + `occlude_box` cortou a ponta do polegar pela metade e deixou resto do botão azul da tela antiga.
O dono aprovou pelo volume, mas pediu registro.

**Regras daqui em diante:**
5. Medir cada canto do quad em grade fina (≤ 25 px) com zoom no canto — nunca na grade do corpo inteiro.
6. `status_bar` só quando o print não tem barra e a área existe no aparelho; na dúvida, 0.
7. Sem dedo sobre a tela (reforça a regra 1). Dedos só na borda do aparelho.
8. `photo-screen.py` agora mede o **anel de 6–16 px fora do quad**: se tiver muitos pixels claros e pouco saturados (tela original aparecendo), avisa `SOBRA DE TELA` por lado. Corrigir até não haver aviso.
9. Revisar cada foto composta com `py -3.12 qa-photo.py <out-id>` (cantos ampliados 1:1) antes de renderizar o post.

**Achado retroativo (19/10):** a checagem nova também acusou `life-patrimonio-iphone` (post de 30/09): fresta da
barra roxa da tela original na base do aparelho. Já publicado; fica como evidência de que a revisão no olho não basta.
