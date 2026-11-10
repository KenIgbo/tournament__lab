import random

def simulate_demo_fixtures(fixtures):
    if not fixtures:
        return []

    demo_fixtures = [fixture.copy() for fixture in fixtures]

    seed = random.randint(1, 1000000)
    rng = random.Random(seed)

    for fixture in demo_fixtures:
        fixture["home_score"] = rng.randint(0, 5)
        fixture["away_score"] = rng.randint(0, 5)
        fixture["status"] = "played"

    return demo_fixtures