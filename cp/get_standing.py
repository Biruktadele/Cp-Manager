import requests
import hashlib
import time
import os

from core.models import Team, User
from . import claculat_rating
from .models import Contest, Standing, TeamStanding

# --- STEP 1: FILL IN YOUR DETAILS ---
# You can set these as environment variables or just paste them here directly.
# To set environment variables:
# On Linux/macOS: export API_KEY="your_key"
# On Windows: set API_KEY="your_key"


def fetch_contest_standings(contest_id , contest_pk):
    API_KEY = "dea57cfc3251ecad3f2e4d839b72df9a0def1451"  # Paste your key here
    API_SECRET = "ff105abb56bd0ce12f60c90c38c63687d289ac58" # Paste your secret here
    CONTEST_ID = str(contest_id) # Paste your mashup's ID here
    # --- Quick check to make sure you filled in the details ---
    if "YOUR_API_KEY" in API_KEY or "YOUR_CONTEST_ID" in CONTEST_ID:
        print("!!! ERROR: Please replace 'YOUR_API_KEY', 'YOUR_API_SECRET', and 'YOUR_CONTEST_ID' in the script before running.")
        return []


    method_name = "contest.standings"
    current_time = int(time.time())
    rand = "123456"  

    api_sig_string = f"{rand}/{method_name}?apiKey={API_KEY}&contestId={CONTEST_ID}&time={current_time}#{API_SECRET}"
    api_sig_hash = hashlib.sha512(api_sig_string.encode('utf-8')).hexdigest()

    api_url = f"https://codeforces.com/api/{method_name}?contestId={CONTEST_ID}&apiKey={API_KEY}&time={current_time}&apiSig={rand}{api_sig_hash}"

    print(f"Fetching standings for contest {CONTEST_ID}...")
    ans = []
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an error for bad responses (like 404 or 500)
        data = response.json()

        if data.get('status') != 'OK':
            print(f"Codeforces API Error: {data.get('comment', 'No comment provided.')}")
            return []

        standings_data = data['result']
        rows = standings_data['rows']

        contest = Contest.objects.get(pk=contest_pk)
        for row in rows:

            handle = row['party']['members'][0]['handle']
            penalty = row['penalty']
            user, created = User.objects.get_or_create(username=handle)
            
            no_solved = sum(1 for p in row['problemResults'] if p.get('points', 0) > 0)
            problem_results_list = []
            rank = row['rank']
            for result in row['problemResults']:
                attempts = ""
                if result.get('points', 0) > 0:
                    if result.get('rejectedAttemptCount', 0) > 0:
                        attempts = f"+{result['rejectedAttemptCount']}"
                    else:
                        attempts = "+"
                elif result.get('rejectedAttemptCount', 0) > 0:
                    attempts = f"-{result['rejectedAttemptCount']}"
                problem_results_list.append(attempts)

            ans.append(Standing(
                user=user,
                contest=contest,
                rank=rank,
                problems_solved=no_solved,
                penalty_time=penalty,
                problemResults=problem_results_list,
                rating_change=0, # Assuming default, adjust if available
                participant_type=row['party']['participantType'],
                is_rated= Standing.objects.filter(user=user , contest=contest).exists()
            ))
        # build a list of participants for the rating calc function
        list_to_insert = []
        for j, i in enumerate(ans):
            list_to_insert.append({
                'handle': i.user.username,
                # ensure a numeric old_rating (default 0 if None)
                'old_rating': getattr(i.user, 'rating', 0) or 0,
                'rank': i.rank,
            })

        res = claculat_rating.calculate_rating_changes(list_to_insert)
        # apply rating deltas back to Standing instances and update User ratings
        for r in res:
            handle = r.get('handle')
            delta = r.get('delta', 0)
            for s in ans:
                if s.user.username == handle:
                    s.rating_change = delta
                    new_rating = (s.user.rating or 0) + delta
                    # print(s , s.)
                    if not s.is_rated and contest.is_rated:
                        User.objects.filter(username=s.user.username).update(rating=new_rating)
        return ans
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in fetch_contest_standings: {e}")
    return []

def Div1_fetch_contest_standings(contest_id , contest_pk):
    API_KEY = "dea57cfc3251ecad3f2e4d839b72df9a0def1451"  # Paste your key here
    API_SECRET = "ff105abb56bd0ce12f60c90c38c63687d289ac58" # Paste your secret here
    CONTEST_ID = str(contest_id) # Paste your mashup's ID here
    # --- Quick check to make sure you filled in the details ---
    if "YOUR_API_KEY" in API_KEY or "YOUR_CONTEST_ID" in CONTEST_ID:
        print("!!! ERROR: Please replace 'YOUR_API_KEY', 'YOUR_API_SECRET', and 'YOUR_CONTEST_ID' in the script before running.")
        return []


    method_name = "contest.standings"
    current_time = int(time.time())
    rand = "123456"  

    api_sig_string = f"{rand}/{method_name}?apiKey={API_KEY}&contestId={CONTEST_ID}&time={current_time}#{API_SECRET}"
    api_sig_hash = hashlib.sha512(api_sig_string.encode('utf-8')).hexdigest()

    api_url = f"https://codeforces.com/api/{method_name}?contestId={CONTEST_ID}&apiKey={API_KEY}&time={current_time}&apiSig={rand}{api_sig_hash}"

    print(f"Fetching standings for contest {CONTEST_ID}...")
    ans = []
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an error for bad responses (like 404 or 500)
        data = response.json()

        if data.get('status') != 'OK':
            print(f"Codeforces API Error: {data.get('comment', 'No comment provided.')}")
            return []

        standings_data = data['result']
        rows = standings_data['rows']

        contest = Contest.objects.get(pk=contest_pk)
        for row in rows:

            teamname = row['party']['teamName']

            penalty = row['penalty']
            team , created = Team.objects.get_or_create(team_name=teamname)
            if not created:
                for m in row['party']['members']:
                    print(m['handle'])
                    user , created = User.objects.get_or_create(username=m['handle'])
                    team.members.add(user)
            no_solved = sum(1 for p in row['problemResults'] if p.get('points', 0) > 0)
            problem_results_list = []
            rank = row['rank']
            for result in row['problemResults']:
                attempts = ""
                if result.get('points', 0) > 0:
                    if result.get('rejectedAttemptCount', 0) > 0:
                        attempts = f"+{result['rejectedAttemptCount']}"
                    else:
                        attempts = "+"
                elif result.get('rejectedAttemptCount', 0) > 0:
                    attempts = f"-{result['rejectedAttemptCount']}"
                problem_results_list.append(attempts)

            ans.append(TeamStanding(
                team_name=team,
                contest=contest,
                rank=rank,
                problems_solved=no_solved,
                penalty_time=penalty,
                problemResults=problem_results_list,
                rating_change=0, # Assuming default, adjust if available
                participant_type=row['party']['participantType'],
                is_rated= TeamStanding.objects.filter(team_name__team_name=team.team_name, contest=contest ).exists()
            ))
        # build a list of participants for the rating calc function
        list_to_insert = []
        for j, i in enumerate(ans):
            list_to_insert.append({
                'handle': i.team_name.team_name,
                # ensure a numeric old_rating (default 0 if None)
                'old_rating': getattr(i.team_name.team_rating, 'rating', 0) or 0,
                'rank': i.rank,
            })

        res = claculat_rating.calculate_rating_changes(list_to_insert)
        # apply rating deltas back to Standing instances and update User ratings
        for r in res:
            handle = r.get('handle')
            delta = r.get('delta', 0)
            for s in ans:
                if s.team_name.team_name == handle:
                    s.rating_change = delta
                    new_rating = (s.team_name.team_rating or 0) + delta
                    # print(s , s.)
                    if not s.is_rated and contest.is_rated:
                        Team.objects.filter(team_name=s.team_name.team_name).update(team_rating=new_rating)
        return ans
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in fetch_contest_standings: {e}")
    return []



