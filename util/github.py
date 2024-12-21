import os
import shutil
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from PIL import Image
from git import Repo
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import subprocess
import sys

def run_gitleaks(user, repo):
    repo_url = f'https://github.com/{user}/{repo}.git'
    output_file = f"{user}_secrets.txt"
    
    cmd = f"chmod +x /app/cmc/gitleaks && /app/cmc/gitleaks --repo-url={repo_url} --report={output_file}"
    subprocess.run(cmd, shell=True)


def count_lines_of_code(repo_path, ext):
    total = 0
    for path, dirs, files in os.walk(repo_path):
        for name in files:
            st.write(name)
            if name.endswith(ext):
                try:  
                    with open(os.path.join(path, name)) as f:
                        total += sum(1 for line in f if line.strip() != '')
                except Exception as e:
                    total =total
    return total

def clone_and_count_lines(user, repo, ext):
    repo_url = f'https://github.com/{user}/{repo}'

    local_path = f'temp/{repo}'
    Repo.clone_from(repo_url, local_path)
    
    lines = count_lines_of_code(local_path, ext)
    
    #shutil.rmtree(local_path)
    # you can add this in the file code after deplyoment in the streamlit ok
    
    return lines

def update_progress_file(filename, repo_name):
    with open(filename, 'a') as f:
        f.write(repo_name + '\n')

def is_repo_processed(filename, repo_name):
    if not os.path.exists(filename):
        st.write("File not found")
        return False
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return repo_name in lines




     # For wide layout
def get_all_user_repos(user):
    page = 1
    repos = []

    while True:
        response = requests.get(f'https://github.com/{user}?page={page}&tab=repositories')
        
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        repo_elements = soup.find_all('a', itemprop='name codeRepository')
        
        if not repo_elements:  # If no more repos found, stop looping
            break

        page_repos = [repo.text.strip() for repo in repo_elements]
        repos.extend(page_repos)
        
        page += 1

    return repos

def get_user_repos(user):
    repo_names = get_all_user_repos(user)
    df = pd.DataFrame(repo_names, columns=['repo_name']) 
    df['repo_size'] = [len(name) for name in df['repo_name']]
    
    return df
