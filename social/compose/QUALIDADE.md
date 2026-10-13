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
