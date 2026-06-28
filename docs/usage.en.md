# Using Prami

Prami is a shared community pet. There is one creature, and everyone looks after it
together by mentioning its Mastodon account.

## Commands

Mention the bot and include one of these words (case does not matter):

| Command | What it does |
|---|---|
| `status` | See how Prami is doing right now |
| `feed` | Give Prami food |
| `play` | Play with Prami |
| `pet` | A little affection |
| `clean` | Clean Prami (it will resent this) |
| `sleep` | Put Prami to bed |
| `wake` | Wake Prami up |
| `help` | List the commands |

Example:

```
@prami feed
@prami status
```

A few aliases also work: `food`, `eat`, `pat`, `cuddle`, `bath`, `wash`, `nap`,
`wakeup`, `?`.

## What Prami tracks

Hunger, happiness, energy, health, cleanliness, social, trust, and chaos — plus whether
it is asleep, its age in days, and a mood derived from all of the above. These values
drift on their own over time: Prami gets hungry, tired, dirty and lonely, so the community
has to keep up. If hunger, cleanliness or energy stay bad for too long, its health starts
to drop.

## Cooldowns

So that one person — or a busy timeline — can't run the pet ragged, each command has a
limit:

| Command | Per user | Globally |
|---|---|---|
| feed | once / 30 min | 10 / hour |
| play | once / 20 min | 15 / hour |
| pet | once / 10 min | 30 / hour |
| clean | once / 60 min | 5 / hour |
| sleep | — | once / 120 min |
| wake | — | once / 60 min |

There is also an overall cap per user per hour and a global cap per hour.

## Sleep

While Prami is asleep, `feed`, `play` and `clean` are gently declined until someone uses
`wake`. Waking it while its energy is very low will get you a complaint, but it will
still wake up.

## Replies and autonomous posts

Replies are unlisted by default so the public timeline stays clean. Prami also posts on
its own from time to time, based on its current mood — also unlisted by default. Both
visibilities are configurable.
