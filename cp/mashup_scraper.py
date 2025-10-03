import requests
import hashlib
import time

# --- Your Details ---
def getcontes(contest_id):
    API_KEY = "dea57cfc3251ecad3f2e4d839b72df9a0def1451"  # Paste your key here
    API_SECRET = "ff105abb56bd0ce12f60c90c38c63687d289ac58" # Paste your secret here
    CONTEST_ID = str(contest_id) # Paste your mashup's ID here

    # --- Building the API Request ---
    current_time = int(time.time())
    method_name = "contest.standings"
    rand = "123456" # A random 6-digit string

    # This is the string that needs to be hashed for the signature
    api_sig_string = f"{rand}/{method_name}?apiKey={API_KEY}&contestId={CONTEST_ID}&time={current_time}#{API_SECRET}"

    # Create the SHA512 hash
    api_sig_hash = hashlib.sha512(api_sig_string.encode('utf-8')).hexdigest()

    # --- Making the Final API Call ---
    api_url = f"https://codeforces.com/api/{method_name}?contestId={CONTEST_ID}&apiKey={API_KEY}&time={current_time}&apiSig={rand}{api_sig_hash}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # --- Now you have the data! ---
        if data['status'] == 'OK':
            contest_info = data['result']
            # You can now process the 'standings' data
            return contest_info["contest"]
        else:
            print(f"API Error: {data['comment']}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")