import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import streamlit as st
from google.cloud import firestore
# Replace with your Firebase project credentials (service account key JSON file)
cred = credentials.Certificate("a.json")

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://profile-data-dde0a-default-rtdb.firebaseio.com/"  # Replace with your database URL
})

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv

def create_user(username, password, codechef_id, leet_id, github_id, codeforces_id, college, category):
    
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

def insert_users_from_input(users_data):
    """Inserts users into Firebase from user input data."""
    if users_data is None:
        return  # nothing to insert
    for user_data in users_data:
        try:
            username, password, codechef_id, leet_id, github_id, codeforces_id, college, category = user_data
            create_user(username, password, codechef_id, leet_id, github_id, codeforces_id, college, category)
        except ValueError:
            print(f"Invalid user data: {user_data}. Skipping.")
        except Exception as e:
            print(f"Error inserting user: {e}. Skipping.")

# if __name__ == "__main__":
#     #users_input = get_user_input()
#     insert_users_from_input([["TUHID", "Sree@1234", "sreecharan9484", "sreecharan9484", "SreeCharan1234", "sreecharan9484","LPU","Student"]])
#     print("Finished inserting users.")


def list_profiles(username): #rt for real time database
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
authenticate_user("Sree Charan" ,"Sree@1234")


# if __name__ == "__main__":
#     usernames = get_all_users()
#     if usernames:
#         print("List of usernames:", usernames)
#print(list_profiles("Sree Charan"))
def listofcollege(db):
    users_ref = db.reference('users')

    # Fetch all data under 'users'
    users_data = users_ref.get()

    # Extract list of colleges
    colleges = set()
    for user_id, user_data in users_data.items():
        if 'college' in user_data:
            colleges.add(user_data['college'])

    # Convert set to list and print
    
    return list(colleges)

print("List of Colleges:", colleges_list)