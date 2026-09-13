# Virtus Social Autopilot — regras permanentes para o Claude Code

## O que é
1 post por dia (imagem + legenda) na Página do Facebook e no Instagram `@virtusappdividendos`, às 18:00 `America/Sao_Paulo`.
Guia completo: `C:\Users\pedro\Downloads\SOCIAL-AUTOPILOT.md`. Respostas da entrevista: `social/PROFILE.md`.
Publisher = GitHub Actions (Opção B). Fila pública = GitHub Pages (`docs/social/`).

## Regras inegociáveis
- Telas de identidade/segurança do Meta (login, checkpoints, Central de Contas, permissões, revelar App Secret): o DONO clica. O Claude descreve o clique, nunca automatiza.
- UM post por dia via API. Nunca postar em lote, nunca "recuperar" vários dias.
- Nunca inventar números, depoimentos, seguidores ou avaliações. Dados demo sempre com "Dados de amostra".
- Nada com tema IA (conteúdo, telas ou hashtags).
- Nunca recomendar compra/venda de ativo específico nem prometer rentabilidade. Preço-alvo e ranking são mostrados como recurso do app, com "Não é recomendação de investimento".
- Legendas citam só números visíveis na imagem.
- Headline ≤ 2 linhas, uma frase em `<em>`, letras miúdas sempre presentes.
- Screenshots reais do app (web via Playwright, Android via adb, iOS via prints das lojas). Nunca recriar telas em HTML.
- Misturar famílias `app` e `life`; rodar plataforma (iPhone / Android / web); não repetir tema na mesma semana.
- Fotos: só Unsplash License; registrar cada uma em `social/compose/photos/credits.json`.
- Aprovação: o dono aprova cada lote de PNGs ANTES do `build.py --queue`.

## Toda sessão, primeiro
1. Ler `social/state.json` (depois de `git pull`).
2. Se `social_state.attempts ≥ 1` hoje → ler `lastError` e corrigir antes de tudo.
3. `queue.future < 3` → produzir 3–7 datados. `bank ≤ 21` → produzir evergreens até ≥ 24.
4. Nunca editar `docs/social/queue.json` à mão; sempre `build.py --queue`.

## Pipeline de reabastecimento
```powershell
cd C:\dev\Virtus\social\compose
py -3.12 build.py ; py -3.12 render.py      # HTML → PNG; abrir e revisar cada PNG; mostrar ao dono
py -3.12 build.py --queue                   # PNGs + queue.json → docs\social
cd C:\dev\Virtus ; git add -A ; git commit -m "social: refill" ; git push
```
Evidência antes de "pronto": `curl.exe "https://pedrofagundesoic.github.io/virtus-social/social/queue.json"` mostra os slugs novos e cada PNG abre pela URL pública.

## Windows
- `curl.exe`, nunca `curl`. URLs entre aspas duplas.
- `py -3.12`, não `python`.
- Segredos: `%USERPROFILE%\.social.env` (fora do repo) + Secrets do GitHub. Este repositório é PÚBLICO: nada de token, senha ou e-mail em arquivo commitado.
