def favourite_worthy(command, before, user):
    if command == "feed" and before["hunger"] >= 80:
        return True
    if command == "pet" and before["social"] <= 20:
        return True
    if command == "clean" and before["cleanliness"] <= 15:
        return True
    return False


def boost_worthy(before_critical, after_critical):
    return before_critical and not after_critical
