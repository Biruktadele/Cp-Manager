import claculat_rating

contest_participants = [
    {'handle': 'ProPlayer',    'old_rating': 2400, 'rank': 3},   # A strong player who underperformed
    {'handle': 'MidPlayer',    'old_rating': 1800, 'rank': 2},   # A mid-level player who did well
    {'handle': 'Newcomer',     'old_rating': 1400, 'rank': 1},   # A new player who won, expecting a large gain
    {'handle': 'StablePlayer', 'old_rating': 1900, 'rank': 4},   # Performed exactly as expected
    {'handle': 'CasualPlayer', 'old_rating': 1600, 'rank': 5},   # A casual player
]

results = claculat_rating.calculate_rating_changes(contest_participants)

for r in results:
    print(r)