# Function to insert data into the database
from firebase_admin import db


def add_user(username, password, codechef_id, leet_id, github_id, codeforces_id, college, category,db):
    
    try:
        
        users_ref = db.reference("users")
        new_user_ref = users_ref.push()
        user_data = {
            "username": username,
            "password": password,
            "codechef_id": codechef_id,
            "leet_id": leet_id,
            "github_id": github_id,
            "codeforces_id": codeforces_id,
            "college": college,
            "category": category
        }
        new_user_ref.set(user_data)
        print(f"User created with ID: {new_user_ref.key}")
        return new_user_ref.key
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

# Function to authenticate a user during login
def authenticate_user(username, password):
    """Authenticates a user against Firebase."""
    try:
        users_ref = db.reference("users")
        users_snapshot = users_ref.get()

        if users_snapshot:
            for user_id, user_data in users_snapshot.items():
                if user_data.get("username") == username and user_data.get("password") == password:
                    print(f"User '{username}' authenticated successfully. User ID: {user_id}")
                    return user_data  # Return the user data if authenticated
            print(f"Authentication failed for user '{username}'.")
            return None  # Return None if authentication fails
        else:
            print("No users found in the database.")
            return None

    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
# Password validation function
def is_valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    return None


def list_profiles(username,db): #rt for real time database
    """Retrieves a user profile from the Realtime Database based on username."""
    try:
        ref = db.reference('/users')
        users = ref.get()

        if users:
            for user_id, user_data in users.items():
                if user_data.get('username') == username:
                    # Convert the dictionary values to a list
                    profile_list = list(user_data.values())
                    return profile_list # Return the list

        return None

    except Exception as e:
        print(f"Error retrieving profile: {e}")
        return None

def listofcollege(db):
    users_ref = db.reference('users')
    users_data = users_ref.get()
    colleges = set()
    for user_id, user_data in users_data.items():
        if 'college' in user_data:
            colleges.add(user_data['college'])    
    return list(colleges)


def totalusers(college_name,n):
    try:
        conn = sqlite3.connect('user_data.db')  # Replace with your database name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE college = ?", (college_name,))
        results = cursor.fetchall()

        college_names = []
        for college in results:
            college_names.append(college[n])

        return college_names

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []

    finally:
        if conn:
            conn.close()    



def listofuser(db):
    """Retrieves all users from Firebase and returns a list of usernames."""
    try:
        users_ref = db.reference("users")
        users_snapshot = users_ref.get()

        if users_snapshot:
            user_data = []
            for user_id, user_info in users_snapshot.items():  # Iterate through user IDs and data
                user_data.append(user_info["username"])  # Append username to the list
            return user_data
        else:
            print("No users found in the database.")
            return []  # Return an empty list if no users are found

    except Exception as e:
        print(f"Error retrieving users: {e}")
        return []  # Return an empty list in case of error
