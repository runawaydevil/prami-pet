from dataclasses import dataclass
from functools import lru_cache

KNOWN_TRAITS = (
    "weird",
    "affectionate",
    "dramatic",
    "suspicious",
    "chaotic",
    "calm",
    "shy",
    "clingy",
    "grumpy",
    "brave",
)


@dataclass(frozen=True)
class Personality:
    traits: frozenset

    def has(self, trait):
        return trait in self.traits

    @property
    def chaos_threshold(self):
        if "chaotic" in self.traits:
            return 55
        if "calm" in self.traits:
            return 82
        return 70

    @property
    def suspicion_threshold(self):
        if "suspicious" in self.traits:
            return 35
        if "affectionate" in self.traits or "clingy" in self.traits:
            return 18
        return 25

    @property
    def tired_threshold(self):
        return 30 if "dramatic" in self.traits else 22

    @property
    def happy_threshold(self):
        return 62 if "affectionate" in self.traits else 70


@lru_cache(maxsize=64)
def from_string(text):
    low = (text or "").lower()
    return Personality(frozenset(t for t in KNOWN_TRAITS if t in low))
