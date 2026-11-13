# Agendador externo do social-daily

O agendamento do GitHub Actions atrasa horas e às vezes não roda (02/11, 11/11 e 12/11 precisaram de disparo manual).
Um serviço externo (cron-job.org) chama a API do GitHub nos horários certos e dispara o mesmo workflow em modo `tick`.

- `tick` só publica entre 18:00 e 23:59 de America/Sao_Paulo e no máximo uma vez por dia. Chamadas repetidas não duplicam post.
- `force` (padrão do botão "Run workflow") publica na hora. Nunca usar `force` no agendador.
- Os agendamentos do próprio GitHub continuam ativos como reserva.

## Chamada

    POST https://api.github.com/repos/pedrofagundesoic/virtus-social/actions/workflows/social-daily.yml/dispatches
    Authorization: Bearer <token>
    Accept: application/vnd.github+json
    X-GitHub-Api-Version: 2022-11-28
    Content-Type: application/json

    {"ref":"main","inputs":{"mode":"tick"}}

Resposta esperada: **204** sem corpo.

## Token

Fine-grained personal access token, só no repositório `virtus-social`, permissão **Actions: Read and write** (o resto sem acesso).
O token fica apenas no cron-job.org. Nunca em arquivo do repositório. Quando expirar, a chamada passa a devolver 401: gerar outro e trocar no cron-job.org.

## Horários (fuso America/Sao_Paulo)

18:05, 18:35, 19:05, 20:05, 21:05 e 22:05, todos os dias.
