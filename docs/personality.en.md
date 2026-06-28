# Prami's personality

Prami is meant to read like a tiny social creature, not a chatbot: cute, strange,
affectionate, dramatic, a little suspicious, occasionally chaotic, never cruel. Replies are
short (1–4 sentences); only `status` runs a touch longer.

## How a reply is chosen

Every reply is a handcrafted template — no generative AI. For each command there are named
template groups, and Prami's current state decides which group to draw from, then picks a
line at random for variety.

| Command | Groups |
|---|---|
| status | normal, hungry, tired, happy, sad, chaotic, dirty, asleep |
| feed | normal, very_hungry, already_full, suspicious, happy, chaotic |
| play | normal, energetic, tired, chaotic, asleep |
| pet | normal, affectionate, low_trust, high_trust, annoyed, asleep |
| clean | normal, dirty, already_clean, angry, chaotic |
| sleep | normal, already_asleep, too_energetic, grateful |
| wake | normal, already_awake, too_tired, annoyed |

Action replies are chosen from the state **before** the command is applied, so feeding a
starving Prami sounds desperate, and feeding a full one sounds unimpressed.

Autonomous posts have their own groups: hungry, lonely, sleepy, chaotic, happy, dirty,
existential, community_appreciation, weird_observation. The current state picks the base
group; sometimes Prami drifts into an existential or weird-observation post instead.

## Personality traits

`PET_PERSONALITY` is free text. Recognised trait words tune the thresholds that pick
groups:

- **chaotic** / **calm** — how easily Prami tips into weirder, chaotic lines
- **suspicious** / **affectionate** / **clingy** — how guarded the care responses are
- **dramatic** — how readily it gets sleepy and theatrical
- **affectionate** — a lower bar for happy/affectionate responses

So `PET_PERSONALITY=chaotic, weird` feels noticeably more feral than
`PET_PERSONALITY=calm, shy`, with the same code and templates.

## Personality packs (future)

Templates live in a pack registry keyed by name (`default` ships today). `PET_PERSONALITY_PACK`
selects which pack is active. Adding a new pack later is just registering another set of
template groups — the selection logic stays the same.
