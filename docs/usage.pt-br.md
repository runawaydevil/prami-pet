# Usando o Prami

O Prami é um bicho de estimação comunitário e compartilhado. Existe uma única criatura, e
todo mundo cuida dela em conjunto mencionando a conta dele no Mastodon.

> Os comandos são sempre em inglês — o Prami só entende essas palavras. Esta documentação
> em português explica como usá-los.

## Comandos

Mencione o bot e inclua uma destas palavras (maiúsculas/minúsculas não importam):

| Comando | O que faz |
|---|---|
| `status` | Mostra como o Prami está agora |
| `feed` | Dá comida ao Prami |
| `play` | Brinca com o Prami |
| `pet` | Um carinho rápido |
| `clean` | Dá banho no Prami (ele vai ficar magoado) |
| `sleep` | Coloca o Prami para dormir |
| `wake` | Acorda o Prami |
| `help` | Lista os comandos |

Exemplo:

```
@prami feed
@prami status
```

Alguns apelidos também funcionam: `food`, `eat`, `pat`, `cuddle`, `bath`, `wash`, `nap`,
`wakeup`, `?`.

## O que o Prami acompanha

Fome, felicidade, energia, saúde, limpeza, sociabilidade, confiança e caos — além de estar
dormindo ou não, a idade em dias e um humor derivado de tudo isso. Esses valores mudam
sozinhos com o tempo: o Prami fica com fome, cansado, sujo e carente, então a comunidade
precisa acompanhar. Se fome, limpeza ou energia ficarem ruins por tempo demais, a saúde
dele começa a cair.

## Tempos de espera (cooldowns)

Para que uma pessoa só — ou uma timeline movimentada — não esgote o bichinho, cada comando
tem um limite:

| Comando | Por usuário | No geral |
|---|---|---|
| feed | 1x / 30 min | 10 / hora |
| play | 1x / 20 min | 15 / hora |
| pet | 1x / 10 min | 30 / hora |
| clean | 1x / 60 min | 5 / hora |
| sleep | — | 1x / 120 min |
| wake | — | 1x / 60 min |

Há também um limite total por usuário por hora e um limite global por hora.

## Sono

Enquanto o Prami está dormindo, `feed`, `play` e `clean` são recusados com gentileza até
alguém usar `wake`. Acordá-lo com a energia muito baixa rende uma reclamação, mas ele
acorda mesmo assim.

## Respostas e posts autônomos

As respostas são `unlisted` (não listadas) por padrão, para não poluir a timeline pública.
O Prami também posta sozinho de vez em quando, conforme o humor do momento — também
`unlisted` por padrão. As duas visibilidades são configuráveis.
