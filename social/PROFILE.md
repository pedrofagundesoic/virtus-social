# Virtus — perfil do Social Autopilot

Respostas da entrevista (brief `SOCIAL-AUTOPILOT.md`, seção 1). Segredos e senhas NUNCA entram aqui:
ficam em `%USERPROFILE%\.social.env` e nos Secrets do GitHub.

## A — Produto
| # | Resposta |
|---|---|
| 1 | **Virtus — Gestão de Patrimônio** (carteira de investimentos com foco em proventos). Web, iOS e Android.<br>Site: https://www.virtusapp.com.br/<br>iOS: https://apps.apple.com/br/app/virtus-gest%C3%A3o-de-patrim%C3%B4nio/id6781425287<br>Android: https://play.google.com/store/apps/details?id=com.correiavirtus.virtus |
| 2 | Sem página escolhedora. Link na bio = site raiz `https://www.virtusapp.com.br/` |
| 3 | Conta demo com dados fictícios (login em `/entrar`). Credenciais só em `.social.env` (`VIRTUS_DEMO_EMAIL`, `VIRTUS_DEMO_PASSWORD`). |
| 4 | Rodapé: **"Crie sua conta gratuita."** + "virtusapp.com.br — link na bio." |

## B — Meta
| # | Resposta |
|---|---|
| 5 | Página do Facebook **ainda não existe** (prevista para ~2026-09-20). |
| 6 | Instagram `@virtusappdividendos` existe; será convertido em conta Profissional (Empresa) e vinculado à Página. |
| 7 | Sem conta em developers.facebook.com (criar na FASE 1). |
| 8 | pt-BR, público Brasil. |

## C — Infra
| # | Resposta |
|---|---|
| 9 | Site/app administrados por terceiro (Railway + Vercel). **O autopilot não depende dessa infra.** |
| 10 | **Opção B**: publisher em GitHub Actions. |
| 11 | Repositório próprio `pedrofagundesoic/virtus-social` (dono = admin). Fila pública via GitHub Pages em `docs/social/`. |
| 12 | Sem banco: estado em `social/state.json`, commitado pelo workflow. |

## D — Regras de publicação
| # | Resposta |
|---|---|
| 13 | **18:00 `America/Sao_Paulo`** (janela 18:00–21:59). |
| 14 | Temas: proventos recebidos · consolidação de carteiras de várias corretoras · calendário de dividendos · yield on cost · preço-alvo · ranking de dividendos · notificações de dividendos.<br>Proibidos: IA; recomendação de compra/venda de ativo específico; promessa de rentabilidade. |
| 15 | Verde-escuro + preto, destaque dourado (do logo). Preto `#070707` · verde `#13271F` · verde barras `#1C4C3C` · dourado `#C4944C`. Logo PNG em `compose/assets/`. |
| 16 | **Sim**: aprovar cada lote antes da fila. Automatizar depois. |

## E — Máquina
| # | Resposta |
|---|---|
| 17 | Windows 11. Git 2.55, Node 24, Python 3.12 (`py -3.12`), gh 2.100, Playwright+Chromium, Pillow, adb. |
| 18 | Android com USB: sim. iPhone: não (usar prints das lojas ou do site em viewport de celular). |
