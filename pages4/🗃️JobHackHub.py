from pathlib import Path
from streamlit_ace import st_ace
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import os
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from streamlit_lottie import st_lottie
import requests 
import sys
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import speech_recognition as sr
from streamlit_extras.echo_expander import echo_expander
from bs4 import BeautifulSoup
global s
k=0
st.set_page_config(page_title="Profile Builder", page_icon='chart_with_upwards_trend', layout="wide", initial_sidebar_state="auto", menu_items=None)
EXAMPLE_NO = 1
recognizer = sr.Recognizer()
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text
def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json() 
def recognize_speech_from_microphone():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
def pseudo_bold(text):
    bold_text = ''.join(chr(0x1D5D4 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else
                        chr(0x1D5EE + ord(c) - ord('a')) if 'a' <= c <= 'z' else c
                        for c in text)
    return bold_text
def streamlit_menu(example=1):
    if example == 1:
        with st.sidebar:
            selected = option_menu(
                menu_title="Job Portal 💼",  # required
                options=["Hackthons", "Jobs", "Exams","Lectures"],  # required
                icons=["bi bi-bag", "bi bi-bag-check-fill", "bi bi-book",],  # optional
                menu_icon="cast",  # optional
                default_index=0,
            )
        return selected
    if example == 2:
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Road Map", "Resume Builder", "Ai bot","ATS-DECTOR"],  # required
                icons=["geo-alt-fill", "file-person-fill", "robot"],  # optional
                menu_icon="cast",  # optional
                default_index=0,
            )
        return selected
    if example == 3:
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Road Map", "Resume Builder", "Ai bot","ATS-DECTOR"],  # required
                icons=["geo-alt-fill", "file-person-fill", "robot"],  # optional
                menu_icon="cast",  # optional
                default_index=0,                
                # optional
            )
        return selected
    if example == 4:
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Road Map", "Resume Builder", "Ai bot","ATS-DECTOR"],  # required
                icons=["geo-alt-fill", "file-person-fill", "robot"],  # optional
                menu_icon="cast",  # optional
                default_index=0,                
                # optional
            )
        return selected
def hactkon():
    url = 'https://hack2skill.com/dashboard/'
    hackathons = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find cards containing hackathon details
        card_elements = soup.find_all('div', class_='card')  # Assuming card structure

        for card in card_elements:
        # Extract data from within each card
            name_element = card.find('div', class_='card-body')  # Customize selector if needed
            name = name_element.get_text(strip=True) if name_element else None

            description_element = card.find('p')  # Adjust selector if necessary
            description = description_element.get_text(strip=True) if description_element else None

            mode_element = card.find('span', class_='text-success')  # Adapt for your mode class
            mode = mode_element.get_text(strip=True) if mode_element else None

            image_element = card.find('img', class_='card-img-top')  # Modify based on image element
            image_url = image_element.get('src') if image_element else None

            # Create and append hackathon dictionary
            hackathons.append({
                'name': name,
                'description': description,
                'mode': mode,
                'image_url': image_url
            })
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return hackathons
selected = streamlit_menu(example=EXAMPLE_NO)
if 'questions' not in st.session_state:
    st.session_state.questions = []
if selected == "Hackthons":
    hackathons=hactkon()
    st.title("Hackathons Listings")

    # Create columns for each hackathon
    for hackathon in hackathons[:]:
        col1, col2, col3 = st.columns([1, 2, 1])

        # Column 1: Image
        with col1:
            st.image(hackathon["image_url"], use_column_width=True)

        # Column 2: Details
        with col2:
            s=hackathon["name"]
            k=hackathon['description'][:5]
            st.header(s[:s.find(k)])
           
            with st.expander("Read more"):
                 st.write(f"**Description :** {hackathon['description']}")  
            st.write(hackathon["mode"])
            

        # Column 3: Apply button
        with col3:
            if st.button("Apply Now", key=hackathon["name"]):
                pass
            
        st.markdown("---")

    # Main content of the Streamlit app
    st.write("Explore and apply to the latest hackathons listed above.")
if selected == "Jobs":

    # Sample data
    hackathons = [
        {
            "name": "Hackathon 1",
            "image_url": "https://via.placeholder.com/150",
            "timeline": "Jan 1, 2024 - Jan 3, 2024",
            "prizes": "1st: $1000, 2nd: $500",
            "details": "This is a brief description of Hackathon 1."
        },
        {
            "name": "Hackathon 2",
            "image_url": "https://via.placeholder.com/150",
            "timeline": "Feb 10, 2024 - Feb 12, 2024",
            "prizes": "1st: $2000, 2nd: $1000",
            "details": "This is a brief description of Hackathon 2."
        },
        {
            "name": "Hackathon 3",
            "image_url": "https://via.placeholder.com/150",
            "timeline": "Mar 15, 2024 - Mar 17, 2024",
            "prizes": "1st: $3000, 2nd: $1500",
            "details": "This is a brief description of Hackathon 3."
        }
    ]

    # Title of the app
    st.title("Hackathon Listings")

    # Create columns for each hackathon
    for hackathon in hackathons:
        col1, col2, col3 = st.columns([1, 2, 1])

        # Column 1: Image
        with col1:
            st.image(hackathon["image_url"], use_column_width=True)

        # Column 2: Details
        with col2:
            st.header(hackathon["name"])
            st.write(f"**Timeline:** {hackathon['timeline']}")
            st.write(f"**Prizes:** {hackathon['prizes']}")
            st.write(hackathon["details"])

        # Column 3: Apply button
        with col3:
            st.button("Apply Now", key=hackathon["name"])

        st.markdown("---")

    # Main content of the Streamlit app
    st.write("Explore and apply to the latest hackathons listed above.")
if selected == "Exams":

    st.title("💬 Chatbot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        

        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        msg=get_gemini_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)        
if selected == "Lectures":

   pass