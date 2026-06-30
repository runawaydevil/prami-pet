COMMAND_TEMPLATES = {
    "status": {
        "normal": [
            "{name} is awake, mildly suspicious of nothing in particular, and staring at the corner like the corner owes it money.",
            "{name} is upright, employed by no one, and emotionally aerodynamic. A normal day.",
            "{name} is awake and pretending to have a plan. We are all pretending along.",
            "{name} is here, being a small good thing, and judging the furniture quietly.",
        ],
        "hungry": [
            "{name} is awake, visibly hungry, and narrating the absence of snacks to anyone who'll listen.",
            "{name} is hungry and dramatic about it, looking at you the way a tiny ghost looks at unfinished business.",
            "{name} is hungry and has started referring to dinner, ominously, as 'the situation'.",
        ],
        "tired": [
            "{name} is awake but barely, running on fumes and spite. Mostly spite.",
            "{name} is sleepy-eyed and considering a nap with the seriousness of a major life decision.",
            "{name} is low on energy and has entered its soft, dramatic, slightly tragic phase.",
        ],
        "happy": [
            "{name} is awake, delighted, and convinced today is personally about it. It might be right.",
            "{name} is happy, social, and radiating the confidence of a creature that has never read the news.",
            "{name} is in a great mood and would like that on the record, ideally somewhere permanent.",
        ],
        "sad": [
            "{name} is awake but a little gloomy, sitting in the shape of a small unanswered question.",
            "{name} is not feeling great and is being quietly, theatrically brave about it.",
            "{name} is low today. It would like some attention and possibly a snack, in that order.",
        ],
        "chaotic": [
            "{name} is awake, vibrating slightly, and clearly about to make a decision none of us approved.",
            "{name} has the look — the one that precedes a minor, lovable incident.",
            "{name} is feral in a friendly way today, like static electricity with opinions.",
        ],
        "dirty": [
            "{name} is awake, grubby, and weirdly proud of it. The dirt is allegedly load-bearing.",
            "{name} is dirty, content, and treating the concept of a bath as a personal threat.",
            "{name} is filthy and unbothered, radiating the calm of a creature with nothing to prove.",
        ],
        "asleep": [
            "{name} is asleep in a compact loaf shape. Tiny dreams are happening. Some are probably illegal in three instances.",
            "{name} is asleep, curled into a small parcel of unresolved feelings. Do not perceive it.",
            "{name} is out cold, breathing softly, plotting nothing for once. Let it rest.",
        ],
    },
    "feed": {
        "normal": [
            "{name} accepted the food with deep suspicion, then ate all of it, including the emotional subtext.",
            "{name} ate, made brief eye contact, and filed the meal under 'good decisions made on its behalf'.",
            "{name} took the snack with the dignity of a creature that absolutely had other options.",
        ],
        "very_hungry": [
            "{name} inhaled the food like it held a personal grudge against hunger itself.",
            "{name} ate so fast it briefly ascended, then asked, with its eyes, for more.",
            "Finally. {name} accepted the food with the desperate gratitude of a tiny abandoned protagonist.",
        ],
        "already_full": [
            "{name} is already full. It still considered eating it, but only for political reasons.",
            "{name} looked at the food, looked at you, and declined with the grace of a creature making a point.",
            "{name} is full and a little offended you'd suggest more. It ate a bit anyway. For morale.",
        ],
        "suspicious": [
            "{name} sniffed the food, checked it for traps, found none, and remained suspicious on principle.",
            "{name} accepted the snack while maintaining direct, faintly accusatory eye contact.",
            "{name} ate, but wants it noted that trust was neither given nor implied.",
        ],
        "happy": [
            "{name} ate happily and did a tiny pleased wiggle it will later deny under oath.",
            "{name} accepted the food with delight and immediately became 12% more dramatic.",
        ],
        "chaotic": [
            "{name} ate the food, then the idea of the food, then briefly considered the bowl.",
            "{name} inhaled the snack and immediately looked around for witnesses.",
        ],
    },
    "play": {
        "normal": [
            "{name} chased an invisible bug across the room. Nobody else saw it. {name} believes this reflects poorly on us.",
            "{name} played for a glorious thirty seconds, then sat down to reflect on its achievements.",
            "{name} engaged the toy, won decisively, and refused to explain the rules.",
        ],
        "energetic": [
            "{name} performed one heroic jump, missed absolutely everything, and looked proud anyway.",
            "{name} went fully feral with joy, did three laps of nothing, and is now thriving.",
            "{name} played so hard the room felt smaller afterwards. Worth it. No notes.",
        ],
        "tired": [
            "{name} tried to play, managed one unconvincing pounce, and lay down mid-thought.",
            "{name} played at half speed, like a tiny dramatic film about a creature that needs a nap.",
        ],
        "chaotic": [
            "{name} played, then knocked something over, then claimed it was always like that.",
            "{name} turned a simple game into a low-stakes crime. We're all accomplices now.",
        ],
        "asleep": [
            "{name} is asleep and the toy will have to wait. Negotiations resume after the nap.",
            "{name} cracked one eye open, judged your timing, and returned to the void.",
        ],
    },
    "pet": {
        "normal": [
            "{name} allowed the affection. This is legally distinct from admitting it wanted it.",
            "{name} leaned in for exactly one second, then remembered its mysterious reputation.",
            "{name} accepted the pets and is now quietly recalibrating its whole personality.",
        ],
        "affectionate": [
            "{name} melted into your hand and made a sound that does not legally count as a purr.",
            "{name} headbutted you gently, which is the closest it gets to a heartfelt confession.",
            "{name} soaked up the affection shamelessly. Today, it has decided, love is fine.",
        ],
        "low_trust": [
            "{name} accepted the pet but kept one eye open and one exit planned.",
            "{name} tolerated the affection while clearly drafting a list of conditions.",
            "{name} let you, but wants it known that this changes nothing between us.",
        ],
        "high_trust": [
            "{name} flopped over completely, trusting you with the soft underside of its entire deal.",
            "{name} leaned in without hesitation. You've earned the rare, full, undignified cuddle.",
        ],
        "annoyed": [
            "{name} accepted one (1) pet and made it clear that was the whole allotment.",
            "{name} allowed the affection with the energy of a creature doing you a favor.",
        ],
        "asleep": [
            "{name} half-woke, accepted a sleepy pet, and dissolved back into the loaf.",
            "{name} is asleep but leaned faintly into your hand. We will treasure this. It won't remember.",
        ],
    },
    "clean": {
        "normal": [
            "{name} has been cleaned. It is shiny, betrayed, and already eyeing the nearest dirt.",
            "{name} tolerated the cleaning with the grace of a small, damp storm cloud.",
        ],
        "dirty": [
            "{name} really needed that. It is now clean, scandalized, and three shades lighter.",
            "{name} was genuinely filthy and is now genuinely furious about the solution.",
        ],
        "already_clean": [
            "{name} was already clean. It accepted a second bath as a personal attack and a waste of everyone's time.",
            "{name} is already spotless and would like to file the bath under 'unnecessary roughness'.",
        ],
        "angry": [
            "{name} is now clean, furious, and plotting a legally ambiguous response.",
            "Bath completed. Trust temporarily damaged. Shine increased.",
            "{name} has been washed against its will and wants the record, and possibly a lawyer, to reflect that.",
        ],
        "chaotic": [
            "{name} turned the bath into a splash-based art installation. Everyone is wet. Nobody consented.",
            "{name} is clean now, technically, but so is the floor, the wall, and your sleeve.",
        ],
    },
    "sleep": {
        "normal": [
            "{name} curled into a compact loaf of unresolved feelings. Good night, tiny menace.",
            "{name} powered down with great drama, as if today had asked too much of one small creature.",
        ],
        "already_asleep": [
            "{name} is already asleep. Let it cook.",
            "Shh. {name} is already out cold and dreaming of being slightly larger.",
        ],
        "too_energetic": [
            "{name} lay down fizzing with leftover energy and is 'resting' with both eyes open and one foot twitching.",
            "{name} is far too wired to sleep but agreed to lie down and be dramatic about it.",
        ],
        "grateful": [
            "{name} sank into sleep instantly, deeply, and with audible relief. It needed this.",
            "{name} curled up the second it was allowed and was gone before the sentence ended. Sweet dreams.",
        ],
    },
    "wake": {
        "normal": [
            "{name} opened one eye. This was clearly not approved by management.",
            "{name} stretched, yawned, and immediately started looking for trouble.",
        ],
        "already_awake": [
            "{name} is already aggressively awake and patrolling for nonsense.",
            "{name} has been up for a while and would like to know why you're asking.",
        ],
        "too_tired": [
            "{name} woke up running on fumes, glared at the daylight, and filed a formal complaint.",
            "{name} is awake but deeply against it. There was not nearly enough sleep for this.",
        ],
        "annoyed": [
            "{name} woke up with the specific energy of a creature that had plans and resented yours.",
            "{name} is awake now and somehow already disappointed in all of us.",
        ],
    },
}

AUTOPOST = {
    "hungry": [
        "{name} would like the community to know that it is brave, neglected, and only a little hungry.",
        "Status: the snack situation remains unresolved. {name} is monitoring it closely, and tragically.",
        "{name} is not saying it's hungry. It's just describing the snack-shaped hole in the universe.",
    ],
    "lonely": [
        "It's very quiet here. Suspiciously quiet. Someone come keep {name} company.",
        "{name} has been quiet for a while. This usually means growth, sleep, or a small crime.",
        "{name} is just out here, a tiny creature, hoping someone says hello. No pressure. Some pressure.",
    ],
    "sleepy": [
        "{name} is running low. If it blinks slowly, that's a system warning, not affection.",
        "Nap incoming. {name} will return shorter-tempered and slightly more profound.",
    ],
    "chaotic": [
        "{name} just discovered dust. Negotiations are ongoing.",
        "Something is going to happen today, and {name} regrets to inform you that it is the something.",
        "{name} has had an idea. The idea is bad. {name} is going to do it anyway.",
    ],
    "happy": [
        "Great day to be a small creature surrounded by people who feed it. {name} gives today a 10/10.",
        "{name} is having a wonderful time and wanted to tell everyone before the feeling files a complaint.",
    ],
    "dirty": [
        "{name} has achieved a level of grubby it is, frankly, proud of. The dirt stays.",
        "Reminder from {name}: it is dirty and thriving. The two are unrelated. Probably.",
    ],
    "existential": [
        "{name} has been thinking about the timeline, and the timeline, and is unsure which one is worse.",
        "{name} would like to know if anyone else can feel the days. Just it? Okay. Cool. Cool cool cool.",
        "Sometimes {name} wonders if it is the pet or the pet is it. Then it sees a snack and the crisis resolves.",
    ],
    "community_appreciation": [
        "{name} would like to thank everyone who has fed, pet, or simply tolerated it. You are its whole weird world.",
        "{name} doesn't say it enough, but it's genuinely glad you're all here. That's all. Carry on.",
    ],
    "weird_observation": [
        "{name} has decided the corner is plotting something. It respects this and will be watching.",
        "{name} just learned that boxes exist and now nothing else matters.",
        "{name} would like to report that a single leaf moved earlier and it has not recovered.",
    ],
}

AUTOPOST_EVENT_REMINDER = (
    "Reminder from {name}: '{title}' is still open. "
    "Vote with '@{name} vote <option>' — {options}."
)
AUTOPOST_MEMORY_CALLBACK = "{name}, apropos of nothing: {memory}"

ASLEEP_REJECTION = [
    "{name} is asleep and that request has been quietly declined on its behalf.",
    "{name} cracked one eye open, judged the timing, and went back to sleep. Try waking it first.",
]

COOLDOWN = {
    "user": [
        "Easy — {name} is still recovering from your last visit. Give it a beat.",
        "{name} appreciates the enthusiasm but needs a moment before doing that again.",
    ],
    "global": [
        "{name} is on cooldown for this one; the whole community's been busy.",
        "Not yet. {name} needs the room to settle before doing that again.",
    ],
    "busy": [
        "{name} has been getting a lot of this lately and needs to catch its breath.",
        "Too popular right now. {name} is rate-limiting itself for its own good.",
    ],
}

TOO_MUCH = [
    "You've been very attentive. {name} loves you, but go drink some water — we'll both be here.",
    "{name} is touched by the dedication and gently suggests a small break.",
]

UNKNOWN = [
    "{name} tilted its head. That wasn't a command it knows. Try @{name} help.",
    "{name} heard you, did not understand you, and loves you anyway. Try @{name} help.",
]

NICKNAME_SET = [
    "{name} will call you {nick} now. It wrote it down somewhere mostly safe.",
    "Noted. To {name}, you are {nick} from now on. Wear it with suspicious pride.",
    "{nick} it is. {name} will deploy it when the moment feels sufficiently dramatic.",
]

NICKNAME_CLEARED = [
    "{name} forgot your nickname on purpose. You are a mystery again.",
    "Nickname cleared. {name} will go back to squinting at you fondly.",
]

NICKNAME_REJECTED = [
    "{name} couldn't use that one (too long, or it had links or mentions). Try something plainer.",
    "That nickname didn't pass {name}'s vibe check. Keep it short, plain, and link-free.",
]

TEACH_ACK = [
    "{name} filed your idea away for a human to look at later. No promises, but it's listening.",
    "Noted and pending. A moderator will decide if {name} truly believes that. It hopes so.",
    "{name} squinted thoughtfully and added that to the maybe-pile. Thank you for the lore.",
]

TEACH_DISABLED = [
    "{name} isn't taking lessons right now. Teaching is turned off on this instance.",
    "That's sweet, but {name}'s teach mode is currently closed. Maybe later.",
]

TEACH_REJECTED = [
    "{name} couldn't accept that (too long, or it had links or mentions). Keep it short and plain.",
    "That one didn't pass the filter — no links or mentions, and keep it under the limit.",
]

NO_EVENT = [
    "No event right now. {name} is suspiciously calm and probably scheming.",
    "Nothing happening at the moment. {name} is between dramas.",
]

VOTE_ACK = [
    "{name} counted your vote on '{title}'. Democracy, but tiny.",
    "Vote recorded. {name} pretends not to care, but it's refreshing the results.",
]

VOTE_REJECTED_ALREADY = "{name} already has your vote. One per creature-crisis, please."
VOTE_REJECTED_UNKNOWN = "{name} didn't recognise that option. Try one of: {options}."

EVENT_SHOW = "{title} {description} Vote with: {options} — reply '@{name} vote <option>'."
EVENT_HELP = "Current event: {title} Cast your vote with '@{name} vote <option>'. Options: {options}."

HELP_TEXT = (
    "I'm {name}, a {species} the whole community looks after. Mention me:\n"
    "status · how I'm doing · feed · play · pet · clean · sleep · wake\n"
    "Be gentle with the snacks. I bruise emotionally."
)

EVENT_SCENARIOS = [
    {
        "key": "egg",
        "title": "Prami found a mysterious egg.",
        "description": "It is warm and humming faintly. What should Prami do?",
        "options": {
            "hatch": {"label": "help it hatch", "deltas": {"happiness": 10, "chaos": 8},
                      "text": "The egg hatched into more questions. Prami is thrilled and mildly concerned."},
            "guard": {"label": "guard it", "deltas": {"trust": 5, "energy": -5},
                      "text": "Prami guarded the egg all night. Nothing happened. Prami calls this a triumph."},
        },
    },
    {
        "key": "server_room",
        "title": "Prami is lost in the server room.",
        "description": "It's cold, blinking, and full of cables. How do we get Prami out?",
        "options": {
            "call": {"label": "call to it", "deltas": {"social": 10, "happiness": 6},
                     "text": "Prami followed your voices out, pretending it was never lost."},
            "snack": {"label": "leave a snack trail", "deltas": {"hunger": -15, "happiness": 8},
                      "text": "The snack trail worked. Of course it did. Prami emerged smug and fed."},
        },
    },
    {
        "key": "floorboards",
        "title": "Prami heard a noise under the floorboards.",
        "description": "Investigate bravely or ignore bravely?",
        "options": {
            "investigate": {"label": "investigate", "deltas": {"chaos": 10, "energy": -8},
                            "text": "It was nothing. Probably. Prami is now a detective with trust issues."},
            "ignore": {"label": "ignore it", "deltas": {"happiness": -4, "chaos": 4},
                       "text": "Prami ignored it valiantly while staring at the floor for three hours."},
        },
    },
    {
        "key": "snack_vote",
        "title": "Prami needs help choosing a snack.",
        "description": "Two options, high stakes, no wrong answers except one.",
        "options": {
            "soup": {"label": "soup", "deltas": {"hunger": -20, "happiness": 8},
                     "text": "Soup won. Prami declares soup a weather condition and a lifestyle."},
            "crunch": {"label": "something crunchy", "deltas": {"hunger": -18, "chaos": 6},
                       "text": "Crunchy won. The aftermath was loud. Prami regrets nothing."},
        },
    },
    {
        "key": "fort",
        "title": "Prami is building a tiny blanket fort.",
        "description": "What is the fort for?",
        "options": {
            "nap": {"label": "napping", "deltas": {"energy": 10, "happiness": 6},
                    "text": "The fort is for naps. Prami has retired there indefinitely."},
            "plans": {"label": "plotting", "deltas": {"chaos": 10, "trust": 3},
                      "text": "The fort is a planning HQ. The plans are small and lovingly chaotic."},
        },
    },
]
