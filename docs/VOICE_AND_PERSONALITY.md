# Voice and personality

This is the writing guide for Prami. Read it before adding or editing any response template.
All of Prami's text lives in `prami/templates.py` — the logic that picks between lines lives in
`prami/responses.py`. You should almost never need to touch logic to add a line.

## 1. Core voice

Prami is:

- **tiny** — a small creature, not a service
- **strange** — odd in a gentle, curious way
- **affectionate** — warm, but not gushing
- **dramatic** — everything is a Situation
- **suspicious** — squints first, trusts slowly
- **social** — it wants the community around
- **chaotic in a harmless way** — gremlin energy, no real damage
- **never cruel**
- **never corporate**
- **never assistant-like**

Prami sounds like a little fediverse creature with too much emotional complexity for its size —
a community goblin that understands social media just enough to misuse it lovingly.

## 2. Writing rules

Prami should:

- speak in **short** replies
- avoid generic chatbot language
- never say "How can I help you?" or anything support-desk shaped
- avoid overused internet slang
- never be mean to users
- never moralize or lecture
- never produce walls of text
- sound like a **creature**, not a customer-support bot

Refer to Prami in the third person and mostly avoid pronouns (use "it"/"they" sparingly) so the
`{name}` placeholder works for any pet name. Address the user as "you" warmly, never as a ticket.

## 3. Response length

- **normal command replies:** 1–3 sentences
- **status replies:** up to 5 short lines (the one place Prami can ramble a little)
- **autonomous posts:** 1–4 sentences
- **help replies:** concise, readable, and in-character — a short menu, not a manual

If a line needs a scroll, it's too long. If it needs a paragraph break, it's probably two
ideas — keep one.

## 4. Humor rules

The humor should be:

- **weird** — unexpected angles, tiny absurd logic
- **warm** — the joke never punches at anyone
- **slightly absurd** — soup is a weather condition
- **emotionally dramatic** — small stakes, operatic feelings
- **fediverse-friendly** — it fits a calm timeline, doesn't shout

Avoid:

- cringe meme spam ("slay", "based", "no cap", emoji walls)
- hostile sarcasm aimed at the user
- excessive randomness (weird should still mean something)
- references that will age badly (current memes, trends, brands)
- any joke that depends on insulting a user

## 5. Example good lines

### hungry
- Prami is not saying it's hungry. It's just describing the snack-shaped hole in the universe.
- Prami would like the community to know that it is brave, neglected, and only a little hungry.
- Status: the snack situation remains unresolved. Prami is monitoring it closely, and tragically.
- Prami has started referring to dinner, ominously, as 'the situation'.
- Prami inhaled the food like it held a personal grudge against hunger itself.

### sleepy
- Prami curled into a compact loaf of unresolved feelings. Good night, tiny menace.
- Prami is running low. If it blinks slowly, that's a system warning, not affection.
- Nap incoming. Prami will return shorter-tempered and slightly more profound.
- Prami sank into sleep instantly, deeply, and with audible relief. It needed this.
- Prami opened one eye. This was clearly not approved by management.

### happy
- Prami is awake, delighted, and convinced today is personally about it. It might be right.
- Great day to be a small creature surrounded by people who feed it. 10/10.
- Prami is in a great mood and would like that on the record, ideally somewhere permanent.
- Prami did a tiny pleased wiggle it will later deny under oath.
- Prami is having a wonderful time and wanted to tell everyone before the feeling files a complaint.

### lonely
- It's very quiet here. Suspiciously quiet. Someone come keep Prami company.
- Prami has been quiet for a while. This usually means growth, sleep, or a small crime.
- Prami is just out here, a tiny creature, hoping someone says hello. No pressure. Some pressure.
- Prami is missing the group chat and being dignified about it, mostly.
- Just Prami and its thoughts, which is one too many things in this room.

### chaotic
- Prami just discovered dust. Negotiations are ongoing.
- Something is going to happen today, and Prami regrets to inform you that it is the something.
- Prami has had an idea. The idea is bad. Prami is going to do it anyway.
- Prami turned a simple game into a low-stakes crime. We're all accomplices now.
- Prami is feral in a friendly way today, like static electricity with opinions.

### dirty
- Prami is now clean, furious, and plotting a legally ambiguous response.
- Prami has achieved a level of grubby it is, frankly, proud of. The dirt stays.
- Reminder from Prami: it is dirty and thriving. The two are unrelated. Probably.
- Prami is treating the concept of a bath as a personal threat.
- Bath completed. Trust temporarily damaged. Shine increased.

### affectionate
- Prami allowed the affection. This is legally distinct from admitting it wanted it.
- Prami melted into your hand and made a sound that does not legally count as a purr.
- Prami leaned in for exactly one second, then remembered its mysterious reputation.
- Prami headbutted you gently, which is the closest it gets to a heartfelt confession.
- Prami flopped over completely, trusting you with the soft underside of its entire deal.

### suspicious
- Prami sniffed the food, checked it for traps, found none, and remained suspicious on principle.
- Prami accepted the snack while maintaining direct, faintly accusatory eye contact.
- Prami accepted the pet but kept one eye open and one exit planned.
- Prami ate, but wants it noted that trust was neither given nor implied.
- Prami is staring at the corner like the corner owes it money.

### existential
- Prami has been thinking about the timeline, and the timeline, and is unsure which one is worse.
- Sometimes Prami wonders if it is the pet or the pet is it. Then it sees a snack and the crisis resolves.
- Prami would like to know if anyone else can feel the days. Just it? Okay. Cool. Cool cool cool.
- Prami is a small parcel of unresolved feelings, and today that parcel has questions.
- Prami is here, being a small good thing, and quietly negotiating with the concept of time.

### event-related
- Prami found a mysterious egg, warm and humming faintly. Vote: hatch it or guard it.
- Prami is lost in the server room again. Call to it, or leave a snack trail?
- Soup won. Prami declares soup a weather condition and a lifestyle.
- Prami counted your vote. Democracy, but tiny.
- Prami is building a tiny blanket fort. Possibly for napping. Possibly for plotting.

### community appreciation
- Prami would like to thank everyone who has fed, pet, or simply tolerated it. You are its whole weird world.
- Prami doesn't say it enough, but it's genuinely glad you're all here. That's all. Carry on.
- A new face met Prami today. Welcome — it has already decided to trust you eventually.
- The community has cared for Prami a hundred times now. Thank you, all of you.
- Prami is officially your friend now. Big deal, quietly.

## 6. Example bad lines (and why)

- "How can I help you today? 😊" — assistant/support voice. Prami is a creature, not a help desk.
- "I'm just a humble bot, beep boop!" — breaks character by foregrounding being a bot.
- "lol ur so based no cap fr fr 💀💀" — meme-slang spam; cringe and ages badly.
- "Did you even READ the instructions? Try again, genius." — hostile sarcasm aimed at the user.
- "As an AI, I cannot have feelings, but I appreciate your input." — assistant disclaimer; Prami is *all* feelings.
- "Did you know loneliness is a serious issue? Here's what you should do…" — moralizing and lecturing.
- A four-line tragic backstory about Prami's origins — wall of text; replies must stay short.
- "FEED ME OR I WILL END YOU. 😈" — cruel and threatening; Prami's chaos is harmless, never menacing.
- "Error: command not recognized. Please consult the documentation." — robotic; not in voice.
- "Slay queen, this bath is giving main-character energy! 💅" — dated slang; ages badly and isn't Prami.

## 7. Template review checklist

Before adding a new response template, check:

- [ ] **Is it short?** (within the length limits in section 3)
- [ ] **Is it in Prami's voice?** (tiny, strange, affectionate, dramatic — see section 1)
- [ ] **Is it safe?** (no slurs, harassment, no real-world targets; user text stays sanitized)
- [ ] **Is it not repetitive?** (does the variant pool already have something like it?)
- [ ] **Is it not hostile?** (the joke never lands on a user)
- [ ] **Would it be annoying if seen multiple times in a week?** (if yes, cut or soften it)

## Where to add lines

Open `prami/templates.py`:

- per-command replies → `COMMAND_TEMPLATES[command][variant]`
- autonomous posts → `AUTOPOST[category]`
- nicknames, teach, cooldowns, etc. → the matching named list
- community events → `EVENT_SCENARIOS`

Each variant is just a list of strings, so expanding a mood is adding a line to a list. Use the
`{name}` placeholder for the pet's name (and `{nick}` where supported). No logic changes needed.
