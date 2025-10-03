import math

# --- CORE RATING CALCULATION FUNCTIONS ---

def get_win_probability(rating_a, rating_b):
    """
    Calculates the probability of player A winning against player B
    using the Elo formula.
    """
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

def get_expected_rank(player, participants_list):
    """
    Calculates the expected rank of a player in a contest.
    Expected Rank = 1 + SUM(P(loss against opponent_j))
    """
    expected_rank = 1.0
    for opponent in participants_list:
        if opponent['handle'] != player['handle']:
            # Probability of our player losing to this opponent
            expected_rank += get_win_probability(opponent['old_rating'], player['old_rating'])
    return expected_rank

def find_performance_rating(actual_rank, participants_list):
    """
    Finds the rating a player would need to have for their expected rank to match
    their actual rank. This is done using a binary search.
    """
    low = 1.0
    high = 8000.0 # A reasonable upper bound for a rating

    # Binary search for 100 iterations to find the performance rating
    for _ in range(100):
        mid = (low + high) / 2.0
        
        # Calculate expected rank if the player had the 'mid' rating
        expected_rank = 1.0
        for opponent in participants_list:
            expected_rank += get_win_probability(opponent['old_rating'], mid)
        
        if expected_rank < actual_rank:
            # The mid rating is too high, resulted in a better expected rank
            high = mid
        else:
            # The mid rating is too low
            low = mid
            
    return (low + high) / 2.0

def calculate_rating_changes(participants):
    """
    The main function to orchestrate the calculation of new ratings for all participants.
    'participants' is a list of dicts, each with 'handle', 'old_rating', and 'rank'.
    """
    
    # K_FACTOR determines the volatility. Lower for more stable ratings.
    # In a real system, this would vary based on a user's contest history.
    K_FACTOR = 0.05
    
    updated_participants = []
    
    # Step 1: Calculate the performance rating for each participant
    for player in participants:
        # Create a temporary list of participants for this calculation
        temp_participants = [{'handle': p['handle'], 'old_rating': p['old_rating']} for p in participants]

        player['performance_rating'] = find_performance_rating(player['rank'], temp_participants)
        updated_participants.append(player)
        
    # Step 2: Calculate the preliminary rating change (delta)
    for player in updated_participants:
        rating_diff = player['performance_rating'] - player['old_rating']
        player['delta'] = K_FACTOR * rating_diff

    # Step 3: Apply inflation control
    # The sum of all rating changes should be zero to prevent rating inflation.
    sum_of_deltas = sum(p['delta'] for p in updated_participants)
    correction = sum_of_deltas / len(updated_participants)
    
    for player in updated_participants:
        player['delta'] -= correction
        
    # Step 4: Calculate final new rating
    for player in updated_participants:
        player['new_rating'] = round(player['old_rating'] + player['delta'])
        
    return updated_participants


# --- SCRIPT EXECUTION ---

if __name__ == "__main__":
    
    # --- YOUR CONTEST DATA GOES HERE ---
    # This is a sample contest. You can replace this with your own data.
    # The list contains dictionaries, each representing a participant.
    # 'rank' must be the final rank in the contest.
    contest_participants = [
        {'handle': 'ProPlayer',    'old_rating': 2400, 'rank': 3},   # A strong player who underperformed
        {'handle': 'MidPlayer',    'old_rating': 1800, 'rank': 2},   # A mid-level player who did well
        {'handle': 'Newcomer',     'old_rating': 1400, 'rank': 1},   # A new player who won, expecting a large gain
        {'handle': 'StablePlayer', 'old_rating': 1900, 'rank': 4},   # Performed exactly as expected
        {'handle': 'CasualPlayer', 'old_rating': 1600, 'rank': 5},   # A casual player
    ]
    
    # Calculate the new ratings
    results = calculate_rating_changes(contest_participants)
    
    # --- PRINT THE RESULTS IN A NICE TABLE ---
    print("-" * 65)
    print(f"{'Handle':<15} | {'Old Rating':>12} | {'Rank':>5} | {'New Rating':>12} | {'Change':>7}")
    print("-" * 65)
    
    # Sort by rank for printing
    results.sort(key=lambda x: x['rank'])
    
    for player in results:
        change = player['new_rating'] - player['old_rating']
        sign = '+' if change >= 0 else ''
        print(f"{player['handle']:<15} | {player['old_rating']:>12} | {player['rank']:>5} | {player['new_rating']:>12} | {sign}{change:>6}")

    print("-" * 65)