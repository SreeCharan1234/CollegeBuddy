# import requests

def get_active_days(username):
    """Fetches and returns total active days for a given LeetCode username in 2024.

    Args:
        username (str): The username of the LeetCode user.

    Returns:
        list: A list containing two elements:
            - The username (str)
            - The total active days in 2024 (int) if successful, or None otherwise.
    """

    url = "https://leetcode.com/graphql"
    query = """
    query userProfileCalendar($username: String!, $year: Int) {
      matchedUser(username: $username) {
        userCalendar(year: $year) {
          totalActiveDays
        }
      }
    }
    """

    variables = {
        "username": username,
        "year": 2024
    }

    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()

        if 'errors' in data:
            print("Error:", data['errors'])
            return None

        total_active_days = data['data']['matchedUser']['userCalendar']['totalActiveDays']
        return [username, total_active_days]

    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
        return None

def get_active_days_for_users(usernames):
    """Calculates total active days for a list of LeetCode usernames in 2024.

    Args:
        usernames (list): A list of LeetCode usernames.

    Returns:
        list: A list of lists, where each inner list contains:
            - The username (str)
            - The total active days in 2024 (int) if successful, or None otherwise.
    """

    results = []
    for username in usernames:
        active_days = get_active_days(username)
        if active_days:
            results.append(active_days)

    return results
# # Example usage
# usernames = ["sreecharan9484", "ykgupta2411", "Tauhid_Neyaz"]  # Replace with your usernames
active_days_list = get_active_days_for_users(usernames)

if active_days_list:
    for username, days in active_days_list:
        print(f"{username}: {days} active days in 2024")
else:
    print("Error fetching active days for some users.")



import requests

def get_leetcode_contest_rating(username):


    url = "https://leetcode.com/graphql"
    query = """
    query userContestRankingInfo($username: String!) {
      userContestRanking(username: $username) {
        rating
      }
    }
    """
    variables = {"username": username}

    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()

        if 'errors' in data:
            print(f"Error for {username}:", data['errors'])
            return None

        contest_ranking = data['data']['userContestRanking']

        if contest_ranking is None:  # Handle cases where user has no rating
            print(f"{username} has no contest rating.")
            return None
        
        rating = contest_ranking.get('rating')
        if rating is None:
            print(f"Rating data is missing for {username}")
            return None

        return rating

    except requests.exceptions.RequestException as e:
        print(f"Request error for {username}:", e)
        return None
    except (KeyError, TypeError) as e:
        print(f"Data processing error for {username}:", e)
        return None


def get_ratings_for_users(usernames):
    """Retrieves contest ratings for a list of usernames.

    Args:
        usernames (list): A list of LeetCode usernames.

    Returns:
        dict: A dictionary where keys are usernames and values are their ratings (or None if an error occurred or no rating exists).
    """
    ratings = {}
    for username in usernames:
        rating = get_leetcode_contest_rating(username)
        ratings[username] = rating
    return ratings

usernames = ["sreecharan9484", "ykgupta2411", "Tauhid_Neyaz"]  # Replace with actual usernames
user_ratings = get_ratings_for_users(usernames)

for user, rating in user_ratings.items():
    if rating is not None:
        print(f"{user}'s contest rating: {rating}")
    else:
        print(f"Could not retrieve contest rating for {user}")
