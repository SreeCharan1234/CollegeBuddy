import sqlite3
import streamlit as st
import re  
def create_table():
    conn = sqlite3.connect("user_data.db")  # Connect to SQLite database
    cursor = conn.cursor()
    # Create a table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            codechef_id TEXT,
            leetcode_id TEXT,
            github_id TEXT,
            codeforces_id TEXT,
            college TEXT,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to insert data into the database
def add_user(username, password, codechef_id, leetcode_id, github_id, codeforces_id, college, category):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, password, codechef_id, leetcode_id, github_id, codeforces_id, college, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, password, codechef_id, leetcode_id, github_id, codeforces_id, college, category))
    conn.commit()
    conn.close()

# Function to authenticate a user during login
def authenticate_user(username, password):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Password validation function
def is_valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    return None


def listofuser():
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('user_data.db')  # Replace 'your_database.db' with your desired database name
        cursor = conn.cursor()

        # Execute the query
        cursor.execute("SELECT username FROM users")

        # Fetch all results
        results = cursor.fetchall()

        user_data = []
        for name in results:
            user_data.append(name[0]) # More efficient than list concatenation

        return user_data

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return [] # Return an empty list in case of an error

    finally:
        if conn:
            conn.close() # Ensure the connection is always closed

def list_profiles(name):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Use parameterized query to prevent SQL injection vulnerabilities
        cursor.execute("SELECT * FROM users WHERE username = ?", (name,))

        result = cursor.fetchone()  # Fetch a single result

        if result:  # Check if a result was found
            ans = list(result)
            return ans
        else:
            return None  # Return None if no profile is found

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None  # Return None in case of an error

    finally:
        if conn:
            conn.close()
def listofcollege():
    try:
        conn = sqlite3.connect('your_database.db')  # Replace with your database name
        cursor = conn.cursor()

        # Use DISTINCT to get unique college names
        cursor.execute("SELECT DISTINCT college_name FROM colleges")

        results = cursor.fetchall()

        college_names = []
        for college in results:
            college_names.append(college[0])

        return college_names

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []

    finally:
        if conn:
            conn.close()