# A personalidade do Prami

O Prami foi feito para soar como um bichinho social, não como um chatbot: fofo, estranho,
afetuoso, dramático, um pouco desconfiado, ocasionalmente caótico, nunca cruel. As respostas
são curtas (1 a 4 frases); só o `status` é um pouco mais longo.

> Os textos do Prami são sempre em inglês. Esta documentação em português explica como o
> sistema funciona.

## Como uma resposta é escolhida

Toda resposta é um template feito à mão — sem IA generativa. Cada comando tem grupos de
templates nomeados, e o estado atual do Prami decide de qual grupo puxar; depois sorteia
uma frase do grupo para dar variedade.

| Comando | Grupos |
|---|---|
| status | normal, hungry, tired, happy, sad, chaotic, dirty, asleep |
| feed | normal, very_hungry, already_full, suspicious, happy, chaotic |
| play | normal, energetic, tired, chaotic, asleep |
| pet | normal, affectionate, low_trust, high_trust, annoyed, asleep |
| clean | normal, dirty, already_clean, angry, chaotic |
| sleep | normal, already_asleep, too_energetic, grateful |
| wake | normal, already_awake, too_tired, annoyed |

As falas de ação usam o estado **antes** de o comando ser aplicado, então alimentar um
Prami faminto soa desesperado, e alimentar um já cheio soa entediado.

Os posts autônomos têm grupos próprios: hungry, lonely, sleepy, chaotic, happy, dirty,
existential, community_appreciation, weird_observation. O estado atual escolhe o grupo base;
às vezes o Prami escapa para um post existencial ou de observação estranha.

## Traços de personalidade

`PET_PERSONALITY` é texto livre. Palavras de traço reconhecidas ajustam os limiares que
escolhem os grupos:

- **chaotic** / **calm** — com que facilidade o Prami pende para falas mais esquisitas/caóticas
- **suspicious** / **affectionate** / **clingy** — quão desconfiadas são as respostas de carinho
- **dramatic** — com que facilidade fica sonolento e teatral
- **affectionate** — barra mais baixa para respostas felizes/afetuosas

Então `PET_PERSONALITY=chaotic, weird` soa bem mais feral que `PET_PERSONALITY=calm, shy`,
com o mesmo código e os mesmos templates.

## Personality packs (futuro)

Os templates ficam num registro de packs por nome (`default` é o que existe hoje).
`PET_PERSONALITY_PACK` seleciona o pack ativo. Adicionar um novo pack depois é só registrar
outro conjunto de grupos de templates — a lógica de seleção continua a mesma.
