def clamp(value, low=0, high=100):
    return max(low, min(high, int(value)))


def compute_mood(pet):
    if pet.asleep:
        return "asleep"
    if pet.health < 25:
        return "unwell"
    if pet.hunger > 75:
        return "ravenous"
    if pet.energy < 20:
        return "exhausted"
    if pet.cleanliness < 25:
        return "filthy"
    if pet.chaos > 75:
        return "feral"
    if pet.happiness > 75 and pet.social > 60:
        return "delighted"
    if pet.social < 20:
        return "lonely"
    if pet.happiness < 30:
        return "grumpy"
    return "content"
