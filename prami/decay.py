import random

from .models import utcnow
from .state import clamp, compute_mood


def tick(pet):
    if pet.asleep:
        pet.energy = clamp(pet.energy + 12)
        pet.hunger = clamp(pet.hunger + 3)
    else:
        pet.energy = clamp(pet.energy - 6)
        pet.hunger = clamp(pet.hunger + 7)

    pet.cleanliness = clamp(pet.cleanliness - 5)
    pet.social = clamp(pet.social - 6)

    strain = 0
    if pet.hunger > 75:
        strain += 3
    if pet.cleanliness < 25:
        strain += 2
    if pet.energy < 15:
        strain += 2

    if strain:
        pet.health = clamp(pet.health - strain)
    elif pet.hunger < 50 and pet.cleanliness > 50 and pet.energy > 40:
        pet.health = clamp(pet.health + 1)

    pet.chaos = clamp(pet.chaos + random.randint(-4, 5))
    pet.mood = compute_mood(pet)
    pet.last_decay_at = utcnow()
    return pet
