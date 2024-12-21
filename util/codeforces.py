import streamlit as st
import requests
import matplotlib.pyplot as plt
def get_user_data(handle):
    base_api_url = "https://codeforces.com/api/"
    url = f"{base_api_url}user.info?handles={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["result"][0]
    else:
        st.error(f"Error: {response.text}")
        return None

def get_contest_data(handle):
    base_api_url = "https://codeforces.com/api/"
    url = f"{base_api_url}user.rating?handle={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.text}")
        return None

def get_submission_data(handle):
    base_api_url = "https://codeforces.com/api/"
    url = f"{base_api_url}user.status?handle={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        st.error(f"Error: {response.text}")
        return None


