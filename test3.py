import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore  # Import for Firestore

# -- Firebase configuration (replace with your credentials) --
cred = credentials.Certificate("a.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://profile-data-dde0a-default-rtdb.firebaseio.com/"  # Replace with your database URL
})

# -- Firestore client initialization (for scalability) --
db = firestore.client()  # Initialize Firestore client

def create_user(username, password, codechef_id, leet_id, github_id, codeforces_id, college, category):
    """
    Creates a new user in the Firebase Realtime Database (or Firestore) and returns the user ID.

    Args:
        username (str): Username for the new user.
        password (str): User's password (consider hashing for security).
        codechef_id (str): User's CodeChef ID (optional).
        leet_id (str): User's LeetCode ID (optional).
        github_id (str): User's GitHub ID (optional).
        codeforces_id (str): User's Codeforces ID (optional).
        college (str): User's college name (optional).
        category (str): User's category (optional).

    Returns:
        str: The ID of the newly created user, or None on error.
    """

    try:
        # Choose either Realtime Database (commented out) or Firestore
        # users_ref = db.reference("users")  # Use for Realtime Database
        users_collection = db.collection("users")  # Use for Firestore

        # Generate a unique ID (consider UUID for better distribution)
        new_user_ref = users_collection.document()  # Use for Firestore

        user_data = {
            "username": username,
            "password": password,  # Consider hashing before storing
            "codechef_id": codechef_id,
            "leet_id": leet_id,
            "github_id": github_id,
            "codeforces_id": codeforces_id,
            "college": college,
            "category": category
        }

        # Use either set() for Realtime Database (commented out) or add() for Firestore
        # new_user_ref.set(user_data)  # Use for Realtime Database
        new_user_ref.set(user_data)  # Use for Firestore

        st.success(f"User created with ID: {new_user_ref.id}")  # Use for Firestore
        return new_user_ref.id  # Use for Firestore

    except Exception as e:
        st.error(f"Error creating user: {e}")
        return None

st.title("Create User")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
codechef_id = st.text_input("CodeChef ID (optional)")
leet_id = st.text_input("LeetCode ID (optional)")
github_id = st.text_input("GitHub ID (optional)")
codeforces_id = st.text_input("Codeforces ID (optional)")
college = st.text_input("College (optional)")
category = st.text_input("Category (optional)")

if st.button("Create User"):
    user_id = create_user(username, password, codechef_id, leet_id, github_id, codeforces_id, college, category)

    if user_id:
        st.success(f"User created successfully! User ID: {user_id}")