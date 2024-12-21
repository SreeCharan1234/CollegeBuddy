import requests
import json

def RQuestion(username, limit=50):
    

    url = f"https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json"
    }

    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            id
            title
            titleSlug
            timestamp
        }
    }
    """

    variables = {
        "username": username,
        "limit": limit
    }

    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data["data"]["recentAcSubmissionList"]
    else:
        return f"Error fetching data: {response.text}"

def skills(username):
  query = """
    query skillStats($username: String!) {
      matchedUser(username: $username) {
        tagProblemCounts {
          advanced {
            tagName
            tagSlug
            problemsSolved
          }
          intermediate {
            tagName
            tagSlug
            problemsSolved
          }
          fundamental {
            tagName
            tagSlug
            problemsSolved
          }
        }
      }
    }
  """

  variables = {"username": username}

  url = "https://leetcode.com/graphql"  # Replace with the actual GraphQL API endpoint
  headers = {"Content-Type": "application/json"}

  response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

  if response.status_code == 200:
    data = json.loads(response.text)
    return data['data']['matchedUser']['tagProblemCounts']
  else:
    print(f"Error fetching data: {response.text}")
    return None

def get_leetcode_data1(username):
    url = "https://leetcode.com/graphql"
    query = """

    query getLeetCodeData($username: String!) {
      userProfile: matchedUser(username: $username) {
        username
        profile {
          userAvatar
          reputation
          ranking
        }
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
          totalSubmissionNum {
            difficulty
            count
          }
        }
      }
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
      }
      recentSubmissionList(username: $username) {
        title
        statusDisplay
        lang
      }
      matchedUser(username: $username) {
        languageProblemCount {
          languageName
          problemsSolved
        }
      }
     
    }
    
    
    """
    variables = {
        "username": username,
        "year": 2024
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    if 'errors' in data:
        print("Error:", data['errors'])
        return None  
    

    return data['data']

def let_Badges(username):
    url = "https://leetcode.com/graphql"
   
    query="""
    query userBadges($username: String!) {
  matchedUser(username: $username) {
    badges {
      id
      name
      shortName
      displayName
      icon
      hoverText
      medal {
        slug
        config {
          iconGif
          iconGifBackground
        }
      }
      creationDate
      category
    }
    upcomingBadges {
      name
      icon
      progress
    }
  }
}

"""
    
    
    variables = {
        "username": username,
        "year": 2024
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    if 'errors' in data:
        print("Error:", data['errors'])
        return None  
    

    return data['data']

def graph(username):
    url = "https://leetcode.com/graphql"
    query="""
    

query userProfileCalendar($username: String!, $year: Int) {
  matchedUser(username: $username) {
    userCalendar(year: $year) {
      activeYears
      streak
      totalActiveDays
      dccBadges {
        timestamp
        badge {
          name
          icon
        }
      }
      submissionCalendar
    }
  }
}
    """  
    
    
    
    
    variables = {
        "username": username,
        "year": 2024
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    
    data = response.json()
    if 'errors' in data:
          print("Error:", data['errors'])
          return None  
      

    return data['data']
