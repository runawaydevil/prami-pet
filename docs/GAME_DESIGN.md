# Prami — Game Design

## 1. What Prami is

Prami is a shared community virtual pet for Mastodon and the wider Fediverse. It lives as a
single Mastodon account and is cared for collectively by everyone on the timeline — there is
one creature, not a private pet per user. People interact with it by mentioning the account
with simple commands, and Prami answers in character.

The goal is a small, charming social creature that feels alive and belongs to the community,
not a command-line tool wearing a costume.

## 2. Core principles

- **Prami should feel alive.** It has an internal state that drifts on its own and a voice
  that changes with how it feels. It is never just echoing fixed text.
- **Community care should matter.** Stats decay over time, so the pet stays healthy only if
  the community keeps showing up to feed, clean, play with, and rest it.
- **Interactions should have consequences.** Every command moves real numbers — overfeeding
  makes it chaotic, neglect hurts its health, baths cost a little happiness.
- **The bot must avoid spam.** Replies are deflected with cooldowns and rate limits, and
  autonomous posts are infrequent and unlisted by default.
- **Replies should be charming, short, and varied.** One to four sentences, handcrafted, and
  randomised so repeated commands don't read identically.
- **The system must be safe and moderation-friendly.** Blocked users, rate caps, dedup of
  processed statuses, and no loops. Nothing user-supplied is ever stored as Prami's voice.

## 3. Pet stats

All stats are integers clamped to 0–100. Their starting values are tuned so a fresh Prami is
content but already a little hungry and in need of company.

| Stat | Meaning | Start |
|---|---|---|
| **hunger** | How hungry Prami is. High is bad; it rises over time and drops when fed. | 40 |
| **happiness** | General mood fuel. Play and affection raise it; baths and neglect lower it. | 60 |
| **energy** | Stamina. Falls while awake, recovers while asleep. | 70 |
| **health** | Long-term wellbeing. Slowly erodes when hunger, cleanliness, or energy stay bad. | 90 |
| **cleanliness** | How clean Prami is. Falls over time; cleaning restores it. | 70 |
| **social** | Need for interaction. Falls over time; play and pets feed it. | 50 |
| **trust** | How much Prami trusts the community. Built slowly through gentle care (pets). | 30 |
| **chaos** | Gremlin energy. Drifts randomly, spikes from overfeeding and rough handling. | 20 |

Two more fields describe the pet rather than measure it:

- **asleep** — whether Prami is currently sleeping. While asleep, energy recovers and active
  care (feed/play/clean) is gently declined.
- **mood** — a single word derived from the stats every tick (e.g. `content`, `ravenous`,
  `exhausted`, `filthy`, `feral`, `delighted`, `lonely`, `grumpy`, `unwell`, `asleep`). Mood
  is what `status` reports and what drives autonomous posts; users never see raw numbers.

## 4. Commands

Mention the bot with one of these words (case-insensitive; a few aliases also work):

- **status** — Reports how Prami is doing as narrative, never as numbers ("mildly hungry,
  emotionally aerodynamic, staring at the corner").
- **feed** — Lowers hunger and nudges happiness; helps health if Prami was genuinely hungry.
  Feeding an already-full Prami makes it chaotic and a bit annoyed.
- **play** — Raises happiness and social, costs energy, adds a little chaos.
- **pet** — Gentle care: builds trust and social and happiness with a small energy cost.
  Low effort, short cooldown — the everyday way to bond with Prami.
- **clean** — Restores cleanliness but costs a little happiness (pets hate baths) and adds
  some chaos.
- **sleep** — Puts Prami to bed if it's awake. While asleep, energy recovers faster.
- **wake** — Wakes Prami up. If its energy is very low, it wakes but complains.
- **help** — A short, in-character list of the commands.

## 5. Cooldowns

Cooldowns exist so one enthusiastic person — or a busy timeline — can't run the pet ragged.
There are two independent layers:

- **Per-user cooldowns** — a minimum interval between uses of a command by the *same* person.
- **Global limits** — a cap on how often a command can succeed across the *whole* community.

Defaults:

| Command | Per user | Globally |
|---|---|---|
| feed | once / 30 min | 10 / hour |
| play | once / 20 min | 15 / hour |
| pet | once / 10 min | 30 / hour |
| clean | once / 60 min | 5 / hour |
| sleep | — | once / 120 min |
| wake | — | once / 60 min |

On top of these, there are blanket caps: a maximum number of commands per user per hour and a
maximum across the whole community per hour. When something is on cooldown, Prami still
replies — it just answers in character instead of acting ("Easy — still recovering from your
last visit").

## 6. State decay

A scheduler ticks on a fixed interval (15 minutes by default) and nudges Prami's state so it
keeps living between interactions:

- Awake, hunger rises and energy falls each tick; asleep, energy recovers and hunger rises
  more slowly.
- Cleanliness and social both drift down — Prami gets grubby and lonely if left alone.
- Health only moves slowly: it erodes when hunger, cleanliness, or energy stay in bad shape,
  and recovers a little when everything is comfortable.
- Chaos drifts up and down at random, so Prami is never perfectly predictable.
- Mood is recomputed from the new numbers at the end of every tick.

The practical effect is that Prami needs ongoing, distributed attention. A pet fed once and
forgotten will slide into hungry, dirty, lonely, and eventually unwell.

## 7. Autonomous posts

Now and then (every 4 hours by default) Prami posts on its own, without being prompted. The
post is chosen from its current state and mood: a hungry Prami fishes for snacks, a lonely
one asks for company, a chaotic one announces an incoming small crime, and sometimes it just
drifts into an existential or weird-observation post.

These posts default to **unlisted** visibility, and so do command replies. Unlisted keeps
Prami off the public/federated firehose so it never floods followers' home timelines or other
instances — people who want it still see it, but the pet doesn't behave like timeline spam.
Visibility is configurable (public / unlisted / direct) for operators who want something else.

## 8. Personality system

Prami's charm comes from *which* handcrafted line it picks. Every command has several named
response groups, and the pet's state selects the group before a random line is drawn from it:

- **hunger** — when very hungry, feed responses turn desperate; when full, they turn
  unimpressed.
- **energy** — low energy makes Prami sleepy and dramatic; high energy makes play energetic.
- **trust** — low trust makes care responses guarded and suspicious; high trust unlocks rare,
  fully undignified affection.
- **chaos** — high chaos pushes responses toward weirder, more feral lines across the board.
- **cleanliness** — being dirty (or suspiciously clean) changes how status and bath replies
  read.
- **mood / asleep** — mood colours `status`; while asleep, most commands get sleepy replies.

For action commands the line is chosen from the state *before* the command applies, so the
reply reflects what motivated it. On top of state, the free-text `PET_PERSONALITY` setting
tunes the thresholds (a `chaotic` Prami tips into chaos sooner; a `suspicious` one stays
guarded longer; a `calm` one rarely goes feral), so the same code and templates can feel like
different creatures. See [personality.en.md](personality.en.md) for details.

## 8b. Relationships and bonds (Social Intelligence Pack — Phase 1)

Prami keeps lightweight, game-only memory about each user — never personal-data profiling,
only interaction data. Per user it tracks total and per-command interaction counts, a
**trust score**, a **bond level**, an optional **user-set nickname**, and first/last seen.

Bond levels progress with kind, repeated care: **stranger → familiar → trusted → friend →
beloved menace**. Each care command adds a little trust (petting most of all); helping while
Prami is in a critical state (very hungry, unwell, filthy, or exhausted) grants a bonus, so
the people who show up in a crisis are remembered as closer.

Relationships gently warm Prami's voice — a known user with a nickname hears it used now and
then, a bit more often at higher bonds. Raw numbers are never exposed in normal replies; they
are only visible through the developer `relationship` CLI command.

Users set their own nickname with `nickname <name>` (aliases: `name me`, `call me`) and clear
it with `nickname clear`. Nicknames are sanitized (max 32 characters; no URLs, mentions, HTML,
or line breaks) and rate-limited.

## 8c. Social Intelligence Pack

These features make Prami feel socially aware while staying safe and moderated. All of the
heavier ones default to **off** and are enabled deliberately per instance.

**Favourites** — Prami's lightweight "I noticed" reaction, and the preferred response to
ordinary good moments: feeding it when starving, petting it when lonely, cleaning it when
filthy, or hitting a milestone. Off unless enabled, capped per hour and per user per day,
never on private statuses unless allowed, never duplicated.

**Boosts** — rare and off by default. Reserved for genuinely special moments (a critical
save, a major milestone, a completed event). Even when enabled they are bounded by a daily
cap, a minimum gap between boosts, and public-only by default. Prami always prefers a
favourite over a boost.

**Relationship memory and bonds** — see section 8b.

**Teach / memory** — users can suggest lore, but nothing becomes part of Prami until an admin
approves it. Approved memories can surface in autonomous posts and flavour. Off unless
enabled. See [MODERATION.md](MODERATION.md).

**Community events** — occasional, lightweight, narrative events ("Prami found a mysterious
egg") that the community votes on with `@prami vote <option>`. One vote per user; the winning
option changes Prami's state; completion produces one autonomous post and, rarely, a boost.

**Milestones** — small community and per-user achievements (first feeding, 100 interactions,
7 days alive, reaching a bond level, a critical save). Each is announced once (unlisted),
some trigger a favourite, and very rare major ones may be boost-eligible.

**Smarter autonomous posts** — Prami's self-posts consider mood, recent state, an active
event, and approved memories, and avoid repeating the same category back-to-back. Categories:
hungry, lonely, sleepy, chaotic, happy, dirty, existential, community appreciation, approved
memory callback, and active event reminder.

**Admin controls** — admins can pause/resume Prami, toggle features, manage blocks, and
review the teach queue at runtime. See [ADMIN_COMMANDS.md](ADMIN_COMMANDS.md).

## 9. Moderation and safety

Prami is designed to be quiet, hard to abuse, and easy to host responsibly:

- **Blocked users** — accounts listed in configuration (or marked blocked) are ignored
  silently; Prami never replies to them.
- **Rate limits** — per-user and global caps, plus per-command cooldowns, bound how much the
  pet can be poked in any window.
- **Ignored / processed statuses** — every status ID Prami acts on is recorded, so it never
  replies to the same mention twice, even across restarts.
- **No loops** — Prami never replies to its own posts and never acts on its own account, so it
  can't get into a reply loop with itself.
- **Unlisted by default** — replies and autonomous posts stay off public timelines unless an
  operator opts in.
- **No user-supplied voice** — the MVP deliberately has **no teach/memory command**. Letting
  the public write what Prami says or remembers is a moderation hazard (it becomes a vector
  for slurs, harassment, or spam in the pet's mouth). That feature is intentionally deferred
  until it can ship with moderator approval gating.

## 10. Future roadmap

Mentioned here as direction, not built in the MVP:

- A **teach / memory system** where the community can suggest things Prami learns, gated
  behind moderator approval.
- **Community voting events** — collective decisions that change Prami or trigger happenings.
- **Items and gifts** — things people can give the pet.
- **Personality packs** — swappable sets of templates and traits (the code already has the
  seam for this).
- **Multiple pets** — more than one creature per instance (the schema already keeps a pet id
  on everything).
- **Pet-to-pet federation** — Pramis on different instances interacting.
- **A web admin / moderation dashboard** — for operators to watch state and manage the pet.

The MVP stays deliberately small: one pet, handcrafted responses, no generative AI, no web
UI. Reliability and a creature that feels alive come first; everything above builds on that.
