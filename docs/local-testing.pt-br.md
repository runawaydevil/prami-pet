# Teste local (sem precisar de Mastodon)

O Prami vem com um CLI local para você brincar com o bicho como engine de jogo e de
personalidade antes de conectá-lo ao Mastodon. O CLI usa o **mesmo** parser, game engine,
cooldowns, banco de dados e gerador de respostas que o bot usa — não é um mock separado.

Por padrão ele usa o `DATABASE_URL` configurado (SQLite é ótimo localmente):

```bash
export DATABASE_URL="sqlite:///prami.db"   # PowerShell no Windows: $env:DATABASE_URL="sqlite:///prami.db"
```

> Os comandos do Prami são em inglês (é o que o parser entende). Esta documentação em
> português explica como usá-los.

## Comandos avulsos

```bash
python -m prami.cli status
python -m prami.cli feed  --user @alice@example.com
python -m prami.cli play  --user @bob@example.com
python -m prami.cli pet   --user @alice@example.com
python -m prami.cli clean --user @alice@example.com
python -m prami.cli sleep --user @alice@example.com
python -m prami.cli wake  --user @alice@example.com
python -m prami.cli help
```

O `--user` é opcional; sem ele, um usuário local padrão é usado. Cada usuário tem seus
próprios cooldowns, como contas de verdade.

## Apelidos e relacionamento

O Prami guarda dados leves e só de jogo sobre cada usuário (contagem de interações, um
trust score por usuário e um nível de vínculo: stranger → familiar → trusted → friend →
beloved menace). Usuários gentis e frequentes criam vínculo mais rápido; ajudar num estado
crítico vale confiança extra.

```bash
python -m prami.cli nickname Soup Wizard --user @alice@example.com   # define apelido
python -m prami.cli nickname clear --user @alice@example.com         # remove o apelido
python -m prami.cli relationship --user @alice@example.com           # inspeciona (só dev)
```

Apelidos são sanitizados (máx. 32 caracteres, sem URLs, menções, HTML ou quebras de linha)
e têm um cooldown curto. O Prami usa o apelido de vez em quando nas respostas, um pouco mais
para usuários de vínculo alto. Os números crus de relacionamento só aparecem no
`relationship`, nunca nas respostas normais.

## Recursos sociais (teach, eventos, admin)

Precisam das flags ligadas (`ENABLE_TEACH_COMMAND`, `ENABLE_EVENTS`). O CLI te concede admin
local. Referência completa: [LOCAL_TESTING.md](LOCAL_TESTING.md).

```bash
python -m prami.cli teach '"Prami believes soup is weather."' --user @alice@example.com
python -m prami.cli admin memories
python -m prami.cli admin approve-memory 1
python -m prami.cli event-start snack_vote
python -m prami.cli vote soup --user @alice@example.com
python -m prami.cli event-complete
python -m prami.cli admin status
```

Quando uma ação é favourite/boost-worthy ou bate um milestone, o CLI mostra isso abaixo da resposta.

## Shell interativo

```bash
python -m prami.cli shell
```

Aí é só digitar as interações como se fossem menções:

```
@alice feed
@bob play
@alice status
@charlie pet
tick 2h
debug
exit
```

Você também pode definir um apelido (`@alice call me Soup Wizard`) e inspecionar um usuário
com `whois @alice`.

Dentro do shell: `tick`, `tick 30m`, `tick 3h` simulam o tempo; `debug` mostra o estado
bruto; `exit` ou `quit` sai.

## Inspecionar o estado bruto (só para dev)

```bash
python -m prami.cli debug-state
```

Mostra os números crus — fome, felicidade, energia, saúde, limpeza, sociabilidade,
confiança, caos, dormindo, humor e o timestamp da última atualização. Usuários normais só
veem o `status` narrativo, nunca esses números.

## Simular a passagem do tempo

```bash
python -m prami.cli tick                 # um passo de decay
python -m prami.cli tick --hours 3
python -m prami.cli tick --minutes 30
```

Aplica exatamente a mesma lógica de decay que o scheduler roda. Um passo equivale a
`STATE_DECAY_INTERVAL_MINUTES` de tempo real, então `--hours 3` aplica a mesma quantidade
de passos que o scheduler aplicaria em três horas.

## Reset

```bash
python -m prami.cli reset          # pede confirmação
python -m prami.cli reset --yes    # sem prompt
```

Volta o bicho aos valores padrão e limpa interações, cooldowns, eventos e status
processados. Os registros de usuários são mantidos.

## Dentro do Docker Compose

Os mesmos comandos funcionam no contêiner, contra o Postgres do Compose:

```bash
docker compose run --rm prami python -m prami.cli status
docker compose run --rm prami python -m prami.cli feed --user @alice@example.com
docker compose run --rm prami python -m prami.cli shell
docker compose run --rm prami python -m prami.cli tick --hours 4
docker compose run --rm prami python -m prami.cli debug-state
```
