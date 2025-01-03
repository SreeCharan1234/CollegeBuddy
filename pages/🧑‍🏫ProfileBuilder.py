import subprocess
import plotly.express as px
from datetime import date
from pathlib import Path
import shutil
import speech_recognition as sr
import pdf2image
import gtts
import sqlite3
import re  
import pandas as pd
import streamlit.components.v1 as components
from local_components import card_container
import json
import traceback
import calplot
from dotenv import load_dotenv
import PIL
import PyPDF2
import re
from streamlit_ace import st_ace
from PIL import Image
import streamlit_shadcn_ui as ui
import base64
from bs4 import BeautifulSoup
from datetime import datetime
import streamlit as st
from streamlit_extras.let_it_rain import rain
from tempfile import NamedTemporaryFile
from streamlit_option_menu import option_menu
from streamlit_extras.mandatory_date_range import date_range_picker
import datetime
import os
import google.generativeai as genai
import matplotlib.pyplot as plt
from IPython.display import display
from local_components import card_container
from IPython.display import Markdown
from streamlit_lottie import st_lottie
import requests 
import sys
import io
import time
import plotly.graph_objects as go
from util.common import get_gemini_response,get_leetcode_data,get_gemini_response1,load_lottieurl
from util.leetcode import get_leetcode_data1, RQuestion, skills, let_Badges, graph,get_active_days_for_users,get_active_days,get_ratings_for_users,get_leetcode_contest_rating
from util.codeforces import get_user_data, get_contest_data
from util.github import run_gitleaks, count_lines_of_code, clone_and_count_lines, is_repo_processed, get_all_user_repos, update_progress_file
from util.login import  add_user, authenticate_user, is_valid_password,listofuser,list_profiles,listofcollege,totalusers
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from google.cloud import firestore
import time

if not firebase_admin._apps:
    cred = credentials.Certificate("a.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://profile-data-dde0a-default-rtdb.firebaseio.com/"
    })
    db = firestore.client() 
# Replace with your Firebase project credentials (service account key JSON file)

global s
k=0
api_key=os.getenv("API-KEY")
genai.configure(api_key=os.getenv("API-KEY"))
t=[ "Python", "Java", "C++", "JavaScript", "Ruby", "PHP", "Swift", "Kotlin", 
    "C#", "Go", "R", "TypeScript", "Scala", "Perl", "Objective-C", "Dart", 
    "Rust", "Haskell", "MATLAB", "SQL", "HTML/CSS", "React", "Angular", "Vue.js", 
    "Node.js", "Django", "Flask", "Spring", "ASP.NET", "Ruby on Rails"]

EXAMPLE_NO = 1


st.set_page_config(page_title="KnowledgeBuilder", page_icon='src/Logo College.png', layout="wide", initial_sidebar_state="auto", menu_items=None)
if "current_theme" not in st.session_state:
    st.session_state.current_theme = "light"

def process_data(data):
    rows = []
    for category, topics in data.items():
        for topic in topics:
            rows.append(
                {"Category": category.capitalize(), "Topic": topic["tagName"], "Problems Solved": topic["problemsSolved"]}
            )
    return pd.DataFrame(rows)
def streamlit_menu(example=1):
    if example == 1:
        with st.sidebar:
            selected = option_menu(
                menu_title="Profile - Builder ",  # required
                options=["Register","Dashboard",  "1vs1","LinkedIn Profile","collage","ATS Detector"],  # required
                icons=["bi bi-person-lines-fill","bi bi-border-all", "bi bi-binoculars-fill", "bi bi-linkedin","bi bi-envelope-at","bi bi-file-person"],  # optional
                menu_icon="cast",  # optional
                 
                default_index=0,
            )
        return selected
     
selected = streamlit_menu(example=EXAMPLE_NO)

if 'questions' not in st.session_state:
    st.session_state.questions = []


if selected == "Register":
    global username
    with st.container(border=True): 
        st.title("Login / Signup")
        option = st.selectbox("Login/Signup/Update", ["Sign up", "Login","Update"])
    
        if option == "Sign up":
                # Input fields
                username = st.text_input("Username", placeholder="Enter your username (must be unique)")
                password = st.text_input("Password", placeholder="Enter your password", type="password")
                with st.container():
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Profile Information")
                        codechef_id = st.text_input("CodeChef ID", placeholder="Enter your CodeChef username")
                        leetcode_id = st.text_input("LeetCode ID", placeholder="Enter your LeetCode username")
                        github_id = st.text_input("GitHub ID", placeholder="Enter your GitHub username")
                        codeforces_id = st.text_input("Codeforces ID", placeholder="Enter your Codeforces username")
                    
                    with col2:
                        st.subheader("Additional Information")
                        predefined_colleges = ["LPU","MIT", "Stanford", "Harvard", "IIT", "Other"]
                        selected_college = st.selectbox("College/School", predefined_colleges)
                        if selected_college == "Other":
                            college = st.text_input("Enter your College/School name")
                        else:
                            college = selected_college

                        category = st.selectbox("Category", ["Student", "Professional", "Other"])

                # Submit button
                if st.button("Create my account"):
                    if username and password and college:
                        # Validate password
                        password_error = is_valid_password(password)
                        if password_error:
                            st.error(password_error)
                        else:
                            try:
                                add_user(username, password, codechef_id, leetcode_id, github_id, codeforces_id, college, category,db)
                                st.success("Account created successfully!")
                            except sqlite3.IntegrityError:
                                st.error("This username is already registered. Please use a different username.")
                    else:
                        st.error("Username, Password, and College are required!")

        elif option == "Login":
                    # Input fields for login
                    st.subheader("Login")
                    username = st.text_input("Username", placeholder="Enter your username for login")
                    password = st.text_input("Password", placeholder="Enter your password", type="password")

                    # Login button
                    if st.button("Login"):
                        if username and password:
                            user = authenticate_user(username, password)
                            if user:
                                st.success(f"Welcome back, {username}!")
                                st.write("Your Profile Information:")
                                st.write(f"- **CodeChef ID:** {user[3]}")
                                st.write(f"- **LeetCode ID:** {user[4]}")
                                st.write(f"- **GitHub ID:** {user[5]}")
                                st.write(f"- **Codeforces ID:** {user[6]}")
                                st.write(f"- **College/School:** {user[7]}")
                                st.write(f"- **Category:** {user[8]}")
                            else:
                                st.error("Invalid username or password.")
                        else:
                            st.error("Both fields are required!")

if selected == "Dashboard":

    link="https://lottie.host/02515adf-e5f1-41c8-ab4f-8d07af1dcfb8/30KYw8Ui2q.json"
    Username = "Sreecharan9484"
    cUsername="Sreecharan9484"
    st.session_state["Username"] = Username
    st.session_state["cUsername"]= cUsername
    l=load_lottieurl(link)
    
    col1, col2 = st.columns([1.3,9])
    
    
    if st.session_state["Username"] and st.session_state["cUsername"]:
        response = requests.get(f'https://www.codechef.com/users/{st.session_state["cUsername"]}')
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            user_info = {}
            user_name_tag = soup.find('div', class_='user-details-container').find('h1')
            user_name = user_name_tag.get_text(strip=True) if user_name_tag else "N/A"
            user_info['Name'] = user_name
            country_tag = soup.find('span', class_='user-country-name')
            country = country_tag.get_text(strip=True) if country_tag else "N/A"
            user_info['Country'] = country
            rating_graph_section = soup.find('section', class_='rating-graphs rating-data-section')
            rating_widget = soup.find('div', class_='widget-rating')
            rating_number = rating_widget.find('div', class_='rating-number')
            ratingc = rating_number.text.strip() if rating_number else None
            #print(ratingc)
            if rating_graph_section:
                contest_participated_div = rating_graph_section.find('div', class_='contest-participated-count')
                if contest_participated_div:
                    no_of_contests = contest_participated_div.find('b').get_text(strip=True)
                    #print(f"No. of Contests Participated: {no_of_contests}")
                    #print(user_info)
                else:
                    print("No. of Contests Participated information not found.")
        data = get_leetcode_data(st.session_state["Username"])
        user_profile = data['userProfile']
        contest_info = data['userContestRanking']
        ko=[]
        for stat in user_profile['submitStats']['acSubmissionNum']:
            ko=ko+[stat['count']]
        with col1:
            st.lottie(l, height=100, width=100)
        with col2:
            st.header(f":rainbow[Student Dashboard]👧👦", divider='rainbow')  
        with st.container(border=True):

            cols = st.columns([1,3,2.5,2.5])
            with cols[0]:
                image = st.image(user_profile['profile']['userAvatar'])

        # Apply CSS to make the image circular
                st.markdown(
                    """
                    <style>
                    .circle-image {
                        border-radius: 50%;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                # Create a link around the image
                image_html = f'<a href="{link}" target="_blank"></a>'
                st.markdown(image_html, unsafe_allow_html=True)
            with cols[1]:
                z=user_info['Name']
                ui.metric_card(title="Name", content=z, description="", key="card1")
            with cols[2]:
                ui.metric_card(title="Top Percentage", content=contest_info['topPercentage'], description="", key="card2")
            with cols[3]:
                ui.metric_card(title="Rating", content=user_profile['profile']['ranking'], description="", key="card3")
        
        
            cols3=st.columns([1.5,1])
            with st.container(border=True):
                with cols3[0]:
                    
                # Data
                    total_questions = ko[0]
                    easy_questions = ko[1]
                    medium_questions = ko[2]
                    hard_questions = ko[3]

                    # Calculate percentages
                    easy_percent = (easy_questions / total_questions) * 100
                    medium_percent = (medium_questions / total_questions) * 100
                    hard_percent = (hard_questions / total_questions) * 100

                    # Create columns for layout
                    col1,  col3 = st.columns([3, 1])

                    # Display total questions
                    
                    with col1:
                            ui.metric_card(title="Total Question ", content=ko[0], key="card9")

                        # Display pie chart
                        
                            fig, ax = plt.subplots()
                            ax.pie([easy_percent, medium_percent, hard_percent],
                                labels=["Easy", "Medium", "Hard"],
                                autopct="%1.1f%%",
                                startangle=140)
                            ax.axis("equal")  # Equal aspect ratio for a circular pie chart
                            st.pyplot(fig)

                        # Display difficulty counts
                    with col3:
                            ui.metric_card(title="Easy ", content=ko[1], key="card12")
                            ui.metric_card(title="Medium", content=ko[2], key="card10")
                            ui.metric_card(title="Hard ", content=ko[3], key="card11")
                
        with st.container(border=True):
            with cols3[1]:
                data1 = {
                    "No of contest": [contest_info['attendedContestsCount'], no_of_contests, 1],
                    "category": ["LeetCode", "CodeChef", "Codeforces"]
                }

                # Vega-Lite specification for the bar graph
                vega_spec = {
                    "mark": {
                        "type": "bar",
                        "cornerRadiusEnd": 4
                    },
                    "encoding": {
                        "x": {
                            "field": "category",
                            "type": "nominal",
                            "axis": {
                                "labelAngle": 0,
                                "title": None,  # Hides the x-axis title
                                "grid": False  # Removes the x-axis grid
                            }
                        },
                        "y": {
                            "field": "No of contest",
                            "type": "quantitative",
                            "axis": {
                                "title": None  # Hides the y-axis title
                            }
                        },
                        "color": {"value": "#000000"},
                    },
                    "data": {
                        "values": [
                            {"category": "LeetCode", "No of contest": contest_info['attendedContestsCount']},
                            {"category": "Code Shef", "No of contest": no_of_contests},
                            {"category": "Codeforces", "No of contest": 1}
                        ]
                    }
                }
                # Display the bar graph in Streamlit
                with card_container(key="chart"):
                    st.vega_lite_chart(vega_spec, use_container_width=True)
            
        with st.container(border=True):
            col1a, col2b= st.columns([1,1]) 
            with st.container(border=True):
                with col1a:
                    with st.container(border=True):
                        st.write("This is resent Question You Did")
                        for language_data in data['matchedUser']['languageProblemCount']:
                            st.write(f"{language_data['languageName']}: {language_data['problemsSolved']}")
                    
            with st.container(border=True):
                with col2b:
                    with st.container(border=True):
                        header = [ "Question Name", "Timestamp"]
                        def format_timestamp(timestamp):
                            dt_object = datetime.datetime.fromtimestamp(int(timestamp))
                            return dt_object.strftime("%Y-%m-%d %I:%M %p")  # AM/PM format
                        processed_data = []
                        for submission in data['recentAcSubmissionList']:
                            formatted_date = format_timestamp(submission['timestamp'])
                            processed_data.append([ submission['title'], formatted_date])
                        df = pd.DataFrame(processed_data, columns=["Question Name", "Timestamp"])
                        st.write(df)

                        # Display table in Streamlit
                        


        a, b,c = st.columns([1,4,1])
        rating = ratingc
        total_contests = no_of_contests
        rank = 1007
        divisio = "Starters 142"
        date = date.today()
        # Left column
        data = {
            "1704067200": 1, "1704153600": 1, "1704240000": 1, "1704326400": 1, "1704412800": 1,
            "1704585600": 15, "1705190400": 1, "1705536000": 1, "1705708800": 3, "1705881600": 2,
            "1705968000": 2, "1706313600": 2, "1706659200": 2, "1707264000": 1, "1707350400": 1,
            "1711497600": 2, "1711929600": 6, "1712016000": 3, "1712361600": 2, "1712707200": 6,
            "1712793600": 2, "1712880000": 1, "1713139200": 3, "1713225600": 3, "1713312000": 2,
            "1713398400": 1, "1713571200": 1, "1716940800": 3, "1717027200": 2, "1717113600": 3,
            "1717200000": 1, "1717286400": 11, "1717459200": 3, "1717718400": 4, "1718841600": 9,
            "1718928000": 3, "1719100800": 1, "1719187200": 2, "1719273600": 5, "1719360000": 1,
            "1719446400": 2, "1719705600": 1, "1719792000": 7, "1719878400": 6, "1719964800": 4,
            "1720051200": 4, "1720137600": 1, "1720224000": 7, "1720310400": 3, "1720483200": 5,
            "1720569600": 5, "1722211200": 1, "1722297600": 1, "1722384000": 1, "1690934400": 2,
            "1691107200": 2, "1691193600": 3, "1694390400": 1, "1694822400": 1, "1694908800": 1,
            "1696723200": 7, "1696982400": 2, "1697328000": 5, "1697414400": 1, "1702512000": 4,
            "1703289600": 7, "1703721600": 3, "1703808000": 3, "1703894400": 1, "1703980800": 3
        }

        # Convert the data to a DataFrame
        df = pd.DataFrame(list(data.items()), columns=['Timestamp', 'Count'])
        df['Date'] = pd.to_datetime(df['Timestamp'].astype(int), unit='s')
        df.set_index('Date', inplace=True)
        daily_counts = df['Count'].resample('D').sum().fillna(0)

        # Create the calendar plot with a brighter colormap
        cmap = 'plasma'  # or 'viridis', 'inferno', etc.
        fig, ax = calplot.calplot(daily_counts, cmap=cmap, figsize=(12, 6),colorbar=False)

        
        # Display the plot in Streamlit
        st.pyplot(fig)
        with a:
            st.metric(label="Rating", value=rating)
            st.metric(label="Total Contests", value=total_contests)
            st.metric(label="Rank", value=rank)
        with b:
            data = {
                'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
                'Rating': [3.5, 4.0, 4.5, 4.2, 4.8]
            }
            df = pd.DataFrame(data)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Week'],
                y=df['Rating'],
                mode='lines+markers',
                name='Rating',
                line=dict(color='royalblue', width=2),
                marker=dict(color='royalblue', size=8)
            ))
            fig.update_layout(
                title='Weekly Ratings',
                xaxis_title='Week',
                yaxis_title='Rating',
                plot_bgcolor='white',
                font=dict(size=14),
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='black',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='black',
                    ),
                ),
                yaxis=dict(
                    showline=True,
                    showgrid=True,
                    showticklabels=True,
                    linecolor='black',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='black',
                    ),
                )
            )
            st.plotly_chart(fig)
        with c:
            st.subheader("Division")
            st.write(f"{divisio}")
            st.subheader("Date")
            st.write(date)

            # Chart (using your preferred charting library)
            # ...
        
        st.markdown("""
            <div style="text-align: center;">
                <p>No of question in each topic</p>
            </div>
        """, unsafe_allow_html=True)
        data = {
            "Arrays": 106,
            "String": 35,
            "HashMap and Set": 30,
            "Dynamic Programming": 28,
            "Sorting": 26,
            "Math": 22,
            "Two Pointers": 21,
            "Matrix": 16,
            "Binary Search": 16,
            "Trees": 14
        }
        st.table(pd.DataFrame(data, index=["Count"]))
        # Convert data to a Pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Count'])

        # Create the bar graph with custom colors
        fig, ax = plt.subplots()
        df.plot(kind='bar', color=['red','blue'], ax=ax)  # Set color to 'skyblue'
        ax.set_title('Topic Counts', color='darkblue')
        ax.set_xlabel('Topic', color='gray')
        ax.set_ylabel('Count', color='gray')
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
        
        linkedin_embed_code = """
            <iframe src="https://www.linkedin.com/embed/feed/update/urn:li:share:7169713233195388928" 
                    height="1115" 
                    width="504" 
                    frameborder="0" 
                    allowfullscreen="" 
                    title="Embedded post">
            </iframe>
            """
        linkedin_embed_code2 = """
            <iframe src="https://www.linkedin.com/embed/feed/update/urn:li:share:7216366908009250816"
                    height="1115" 
                    width="504" 
                    frameborder="0" 
                    allowfullscreen="" 
                    title="Embedded post">
            </iframe>
            """
            # Embed the LinkedIn post in the Streamlit app
        with st.container(border=True):  
            col1, col2 = st.columns([1,1])  
            with st.container(border=True):
                with col1:
                    components.html(linkedin_embed_code, height=1200)  # Adjust height as needed
            with st.container(border=True):
                with col2:
                    components.html(linkedin_embed_code2, height=1200)  # Adjust height as needed
        st.pyplot(fig)

        
    else:
        st.write("## Write Your UserName")

if selected == "ATS Detector":
    
    def input_pdf_setup(uploaded_file):
        if uploaded_file is not None:
            ## Convert the PDF to image
            images=pdf2image.convert_from_bytes(uploaded_file.read())
            first_page=images[0]
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
                }
            ]
            return pdf_parts
        else:
            raise FileNotFoundError("No file uploaded")
    lott=load_lottieurl("https://lottie.host/6a18ec99-538f-48b7-b9f1-85549bfbc5e1/n6lDQ3tHy2.json") 
    col1, col2,clo3= st.columns([2,5,1])
    with col2:
        st.header(f"Applicant Tracking System ", divider='rainbow')
    with col1:
        if lott:
            st_lottie(lott, key="ad", height="150px",width="150px")
        else:
            st.error("Failed to load Lottie animation.")
    with clo3   :
        pass
    with st.container(border=True):
        input_text=st.text_area("Job Description : ",key="input")
        uploaded_file=st.file_uploader("Upload your resume (PDF)",type=["pdf"])
        if uploaded_file is not None:
            st.write("PDF Uploaded Successfully")
        col1, col2 ,col3,clo4= st.columns([2,2.5,2,2])  # Create two columns
        with col1:
            pass
        with col2:
            
            submit1 = st.button("Tell Me About the Resume",type="primary", help="Know your resume",use_container_width=True)
        with col3:
            submit3 = st.button("Percentage match",type="primary", help="Percentage match",use_container_width=True)
        with clo4:
            pass

        #submit2 = st.button("How Can I Improvise my Skills")

        

        input_prompt1 = """
        You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
        Please share your professional evaluation on whether the candidate's profile aligns with the role. 
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """

        input_prompt3 = """
        You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
        your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
        the job description. First the output should come as percentage and then keywords missing and last final thoughts.
        """

        if submit1:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response1(input_prompt1,pdf_content,input_text)
                st.subheader("The Repsonse is")
                st.write(response)
            else:
                st.write("Please uplaod the resume")

        elif submit3:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response1(input_prompt3,pdf_content,input_text)
                st.subheader("The Repsonse is")
                st.write(response)
            else:
                st.write("Please uplaod the resume")

if selected == "LinkedIn Profile":
    
    def extract_text_from_pdf(file):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text

    link="https://lottie.host/a2aa0932-646a-40a0-9638-4634d3a77c89/MU89CSP8h1.json"
    l=load_lottieurl(link)
    col1, col2 = st.columns([1.3,9])  # Create two columns
    with col1:
        st.lottie(l, height=100, width=100)
    with col2:
        st.header(f":rainbow[Linkdin Profile Builder]👧👦", divider='rainbow')
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            # PDF upload
            uploaded_image = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])
            if uploaded_image is not None:
                with st.container(border=True):
                    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
            uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
            if uploaded_file is not None:
                text2 = extract_text_from_pdf(uploaded_file)
            # Job role selection
            job_roles = [
                "Software Engineer",
                "Data Scientist",
                "Product Manager",
                "Designer",
                "Front-end Developer",
                "Back-end Developer",
                "Full-stack Developer",
                "Mobile App Developer",
                "DevOps Engineer",
                "Quality Assurance Engineer",
                "Data Analyst",
                "Business Intelligence Analyst",
                "Machine Learning Engineer",
                "Data Engineer",
                "Product Owner",
                "Product Marketing Manager",
                "Project Manager",
                "Scrum Master",
                "UX Researcher",
                "IT Project Manager",
                "Machnical Engineer",
            ]
            # selected_role = st.selectbox("Select your job role", job_roles)
            selected_role = st.text_input("Which topic you want to learn",placeholder="Enter the topic")
            # Display selected job role
        with col2:
            # Video upload
            st.video(r"Recording 2024-08-03 001234.mp4")

    with st.container(border=True):
            st.markdown(":grey[Click the button to analyze the image]")
            know = st.button("ANALYZE",
                    type="primary", help="Analyze the LinkedIn proflie",use_container_width=True)
    if know:
        
        st.caption("Powerd by Gemini Pro Vision")
        img_=uploaded_image
        img = PIL.Image.open(img_)   
        def get_analysis(prompt, image):
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            # Set up the model
            generation_config = {
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 5000,
            }

            safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
            ]

            model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)

            response = model.generate_content([prompt, image])

            return response.text
        role = """
        You are a highly skilled AI trained to review LinikedIn profile photos and provide feedback on their quality. You are a professional and your feedback should be constructive and helpful.
        """
        instructions = """
        You are provided with an image file depicting a LinkedIn profile photo.

        Your job is to proved a structured report analyzing the image based on the following criteria:

        1. Resolution and Clarity:

        Describe the resolution and clarity of the image. Tell the user whether the image is blurry or pixelated, making it difficult to discern the features. If the image is not clear, suggest the user to upload a higher-resolution photo.
        (provide a confidence score for this assessment.)

        2. Professional Appearance:

        Analyse the image and describe the attire of the person in the image. Tell what he/she is wearing. If the attire is appropriate for a professional setting, tell the user that their attire is appropriate for a professional setting. If the attire is not appropriate for a professional setting, tell the user that their attire might not be suitable for a professional setting. If the attire is not appropriate for a professional setting, suggest the user to wear more formal clothing for their profile picture. Also include background in this assessment. Describe the background of the person. If the background is simple and uncluttered, tell the user about it, that it is  allowing the focus to remain on them. If the background is not good, tell the user about it. If the background is not suitable, suggest the user to use a plain background or crop the image to remove distractions.
        (provide a confidence score for this assessment.)

        3. Face Visibility:

        Analyse the image and describe the visibility of the person's face. If the face is clearly visible and unobstructed, tell the user that their face is clearly visible and unobstructed. If the face is partially covered by any objects or hair, making it difficult to see the face clearly, tell the user about it. Also tell where the person is looking. If the person is looking away, suggest the user to look into the camera for a more direct connection.
        (provide a confidence score for this assessment.)

        4. Appropriate Expression:

        Describe the expression of the person in the image. If the expression is friendly and approachable, tell the user about it. If the expression is overly serious, stern, or unprofessional, tell the user user about it. If the expression is not appropriate, suggest the user to consider a more relaxed and natural smile for a more approachable look.
        (provide a confidence score for this assessment.)

        5. Filters and Distortions:

        Describe the filters and distortions applied to the image. If the image appears natural and unaltered, tell the user about it. If the image appears to be excessively filtered, edited, or retouched, tell the user about it. If the image is excessively filtered, edited, or retouched, suggest the user to opt for a natural-looking photo for a more genuine impression.
        (provide a confidence score for this assessment.)

        6. Single Person and No Pets:

        Describe the number of people and pets in the image. If the image contains only the user, tell the user about it. If the image contains multiple people or pets, tell the user about it. If the image contains multiple people or pets, suggest the user to crop the image to remove distractions.
        (provide a confidence score for this assessment.)

        Final review:

        At the end give a final review on whether the image is suitable for a LinkedIn profile photo. Also the reason for your review.
        """
        output_format = """
        Your report should be structured like shown in triple backticks below:

        ```
        **1. Resolution and Clarity:**\n[description] (confidence: [confidence score]%)

        **2. Professional Appearance:**\n[description] (confidence: [confidence score]%)

        **3. Face Visibility:**\n[description] (confidence: [confidence score]%)

        **4. Appropriate Expression:**\n[description] (confidence: [confidence score]%)

        **5. Filters and Distortions:**\n[description] (confidence: [confidence score]%)

        **6. Single Person and No Pets:**\n[description] (confidence: [confidence score]%)

        **Final review:**\n[your review]
        ```

        You should also provide a confidence score for each assessment, ranging from 0 to 100.

        Don't copy the above text. Write your own report.

        And always keep your output in this format.

        For example:

        **1. Resolution and Clarity:**\n[Your description and analysis.] (confidence: [score here]%)

        **2. Professional Appearance:**\n[Your description and analysis.] (confidence: [socre here]%)

        **3. Face Visibility:**\n[Your description and analysis.] (confidence: [score her]%)

        **4. Appropriate Expression:**\n[Your description and analysis.] (confidence: [score here]%)

        **5. Filters and Distortions:**\n[Your description and analysis.] (confidence: [score here]%)

        **6. Single Person and No Pets:**\n[Your description and analysis.] (confidence: [score here]%)

        **Final review:**\n[Your review]

        """
        prompt = role + instructions + output_format
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": img
            }
        ]
        
        with st.container(border=True):
                st.markdown(":grey[Click the button to analyze the image]")

                
                    # show spinner while generating
                with st.spinner("Analyzing..."):

                        try:
                            # get the analysis
                            analysis = get_analysis(prompt, img)
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                            
                        else:

                            # find all the headings that are enclosed in ** **
                            headings = re.findall(r"\*\*(.*?)\*\*", analysis)

                            # find all the features that are after ** and before (confidence
                            features = re.findall(r"\*\*.*?\*\*\n(.*?)\s\(", analysis)

                            # find all the confidence scores that are after (confidence: and before %)
                            confidence_scores = re.findall(r"\(confidence: (.*?)\%\)", analysis)

                            # find the final review which is after the last confidence score like this:
                            # (confidence: 50%)\n\n(.*?)
                            
                            st.subheader(":blue[LinkedIn] Profile Photo Analyzer", divider="gray")
                            for i in range(6):

                                st.divider()

                                st.markdown(f"**{headings[i]}**\n\n{features[i]}")

                                # show progress bar
                                st.progress(int(confidence_scores[i]), text=f"confidence score: {confidence_scores[i]}")

                            st.divider()
                            st.divider()
                            st.divider()
                            text2 = extract_text_from_pdf(uploaded_file)
                            st.subheader(":blue[LinkedIn] Skills Analyzer", divider="gray")
                            s=f"""Take on the role of a skilled HR professional. Analyze the provided candidate text ({text2}) and compare the candidate's skills to the required skills for the specified job profile ({selected_role}). Identify the top 5 most relevant skills required for the job and determine the candidate's skill gap.Calculate a percentage match based on the overlap between the candidate's skills and the required skills.
                            """+"""Output the results in the following format:
                                1. skils Methoned By user:
                                2. Top Skills Required: {skill1}, {skill2}, {skill3}, {skill4}, {skill5}
                                3. Candidate's Skill Gap: {missing_skills}
                                4 .Role Match Percentage: {percentage} 
                                tell we what you think about the skills of  the useres 
                                """
                            
                            st.write(get_gemini_response(s))

                            st.divider()
                            st.divider()
                            st.divider()
                            st.subheader(":blue[LinkedIn] Certificates Analyzer", divider="gray")
                            s=f"""Take on the role of a skilled HR professional. Analyze the provided candidate text ({text2}) and compare the candidate's Certifications to the required Certifications for the specified job profile ({selected_role}). Identify the top 5 most relevant skills required for the job and determine the candidate's skill gap.Calculate a percentage match based on the overlap between the candidate's skills and the required skills.
                            """+"""Output the results in the following format:
                                1. Certifications Methoned By user:
                                2. Top Certifications Required: {skill1}, {skill2}, {skill3}, {skill4}, {skill5}
                                3. Candidate's Certifications Gap: {missing_skills}
                                4 .Role Match Percentage: {percentage} 
                                tell we what you think about the Certifications of  the useres 
                                """
                            st.write(get_gemini_response(s))

                            st.divider()
                            st.divider()
                            st.divider()   
                            st.subheader(":blue[LinkedIn] Headline Analyzer", divider="gray")
                            s=f"""Take on the role of a skilled HR professional. Analyze the provided candidate text ({text2}) and compare the candidate's Headline to the required Headline for the specified job profile ({selected_role}). Identify the top 5 most relevant skills required for the job and determine the candidate's skill gap.Calculate a percentage match based on the overlap between the candidate's skills and the required skills.
                            """+"""Output the results in the following format:
                                1. Headline Methoned By user:
                                2. Suugest some more text by annalysis: {Headline1}, {Headline2}, {Headline3}, {Headline4}, {Headline5}
                                3. Candidate's Headline Gap (missing words): {missing_words}
                                4 .Role Match Percentage: {percentage} 
                                tell we what you think about the Headline of  the useres 
                                """
                            st.write(get_gemini_response(s))
                            st.divider()
                            st.divider()
                            st.divider() 
                            st.subheader(":blue[LinkedIn] Summary Analyzer", divider="gray")
                            s=f"""Take on the role of a skilled HR professional. Analyze the provided candidate text ({text2}) and compare the candidate's Summary to the required Summary for the specified job profile ({selected_role}). Identify the top 5 most relevant skills required for the job and determine the candidate's skill gap.Calculate a percentage match based on the overlap between the candidate's skills and the required skills.
                            """+"""Output the results in the following format:
                                1. Summary Methoned By user:
                                
                                2. Candidate's Summary Gap: {missing_skills}
                                3 .Role rating you give: {percentage} 
                                tell we what you think about the Summary of  the useres 
                                """
                            st.write(get_gemini_response(s))
                            
                            
                            st.divider()
                            st.divider()
                            st.divider()
                            st.subheader(":blue[LinkedIn] Education Analyzer", divider="gray")
                            s=f"""Take on the role of a skilled HR professional. Analyze the provided candidate text ({text2}) and compare the candidate's Education to the required Education for the specified job profile ({selected_role}). Identify the top 5 most relevant skills required for the job and determine the candidate's skill gap.Calculate a percentage match based on the overlap between the candidate's skills and the required skills.
                            """+"""Output the results in the following format:
                                1. Education Methoned By user:
                                
                                2. Candidate's Education Gap: {missing_skills}
                                3 .Role rating you give: {percentage} 
                                tell we what you think about the Education of  the useres 
                                """
                            st.write(get_gemini_response(s))
                            st.divider()
                            st.divider()
                            st.divider()
                            
        with st.container(border=True):
            pass           

if selected=="1vs1":
    link="https://lottie.host/02515adf-e5f1-41c8-ab4f-8d07af1dcfb8/30KYw8Ui2q.json"
    l=load_lottieurl(link)
    col1, col2 = st.columns([1.3,9])
    with col1:
            st.lottie(l, height=100, width=100)
    with col2:
            st.header(f":rainbow[Compare with your friend]👧👦", divider='rainbow')

    ans=listofuser(db)
    left,right=st.columns(2)
    your_id,friends_id="",""
    with left:
        your_id = st.multiselect("What is your ?", ans, [], placeholder="Select Your's Id")  
    with right:
        friends_id = st.multiselect("What is your friend's?", ans, [], placeholder="Select Your Friend's Id")
   
    if your_id and friends_id:
        
        your_id = list_profiles(your_id[0],db)
        friends_id = list_profiles(friends_id[0],db)
      
        your_data = get_leetcode_data1(your_id[5])
        friend_data = get_leetcode_data1(friends_id[5])
        your_RQuestion=RQuestion(your_id[5], limit=50)
        friend_RQuestion=RQuestion(friends_id[5], limit=50)
        your_let_Badges=let_Badges(your_id[5])
        friend_let_Badges=let_Badges(friends_id[5]) 
        your_skils=skills(your_id[5])
        friend_skils=skills(friends_id[5])
        your_graph=graph(your_id[5])
        friend_graph=graph(friends_id[5])
        my_df = process_data(your_skils)
        friends_df = process_data(friend_skils)
        link="https://lottie.host/3de1b5f0-49df-47f6-8a9b-21d9830c1810/IxEWj5DLSb.json"
        
        l=load_lottieurl(link)
        col1, col2 = st.columns([1.3,9])
        with col1:
                st.lottie(l, height=100, width=100)
        with col2:
                st.header("Coding Platform analyzer 💻💻", divider=True)
        your, midle, friend = st.columns([1.6,0.1, 1.6])
        with your:           
            user_profile = your_data['userProfile']
            contest_info = your_data['userContestRanking']           
            ko=[]
            for stat in user_profile['submitStats']['acSubmissionNum']:
                ko=ko+[stat['count']]
            cols = st.columns([1,2.9])
            with cols[0]:
                    image = st.image(user_profile['profile']['userAvatar'])
            st.markdown(
                    """
                    <style>
                    .circle-image {
                        border-radius: 50%;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                # Create a link around the image
            image_html = f'<a href="{link}" target="_blank"></a>'
            st.markdown(image_html, unsafe_allow_html=True)
            with cols[1]:
                    z=your_data['userProfile']['username']
                    ui.metric_card(title="User Name", content=z, description="", key="card1")
            perc,ratong = st.columns([1,1])
            with perc:
                ui.metric_card(title="Top Percentage", content=contest_info['topPercentage'], description="Great🥰", key="card2")
            with ratong:
                ui.metric_card(title="Rating", content=user_profile['profile']['ranking'], description="Good😁", key="card3")         
            st.header("Easy-Medium-Hard😊😑😥", divider=True)
            total_questions = ko[0]
            easy_questions = ko[1]
            medium_questions = ko[2]
            hard_questions = ko[3]
                # Calculate percentages
            easy_percent = (easy_questions / total_questions) * 100
            medium_percent = (medium_questions / total_questions) * 100
            hard_percent = (hard_questions / total_questions) * 100
                  # Display total questions
            col1,  col3 = st.columns([3, 1])  
            with col1:
                            ui.metric_card(title="Total Question ", content=ko[0], key="card9")

                        # Display pie chart
                        
                            fig, ax = plt.subplots()
                            ax.pie([easy_percent, medium_percent, hard_percent],
                                labels=["Easy", "Medium", "Hard"],
                                autopct="%1.1f%%",
                                startangle=140)
                            ax.axis("equal")  # Equal aspect ratio for a circular pie chart
                            st.pyplot(fig)

                      # Display difficulty counts
            with col3:
                            ui.metric_card(title="Easy ", content=ko[1], key="card12")
                            ui.metric_card(title="Medium", content=ko[2], key="card10")
                            ui.metric_card(title="Hard ", content=ko[3], key="card11")        
            
            st.header("SkillTracker🤹‍♂️🦾", divider=True)
            categories = list(my_df["Category"].unique())
            selected_categories = st.multiselect("Select Categories for Your Data", categories, default=categories, key="my_categories")

            # Filter and Sort Data
            filtered_my_df = my_df[my_df["Category"].isin(selected_categories)]
            sorted_my_df = filtered_my_df.sort_values(by="Problems Solved", ascending=False)

            # Bar Chart
            
            fig, ax = plt.subplots(figsize=(6, 4))
            for category in sorted_my_df["Category"].unique():
                category_data = sorted_my_df[sorted_my_df["Category"] == category]
                ax.bar(category_data["Topic"], category_data["Problems Solved"], label=category)

            ax.set_ylabel("Problems Solved")
            ax.set_xlabel("Topic")
            ax.set_title("Your Problems Solved (Sorted)")
            ax.legend()
            plt.xticks(rotation=90, ha="right")
            st.pyplot(fig)
            # Detailed Data
            st.subheader("Detailed Data View")
            st.dataframe(sorted_my_df)            
            language_data = your_data['matchedUser']['languageProblemCount']
            language_df = pd.DataFrame(language_data)
            language_df.columns = ["Language", "Problems Solved"]
            st.header("Questions per Language🤠", divider=True)
            st.table(language_df)
            header = [ "Question Name", "Timestamp"]
            def format_timestamp(timestamp):
                                dt_object = datetime.datetime.fromtimestamp(int(timestamp))
                                return dt_object.strftime("%Y-%m-%d %I:%M %p")  # AM/PM format
            processed_data = []                        
            for submission in your_RQuestion:
                                formatted_date = format_timestamp(submission['timestamp'])
                                processed_data.append([ submission['title'], formatted_date])
            df = pd.DataFrame(processed_data, columns=["Question Name", "Timestamp"])
            st.header("Your Recent Question😊📕📅",divider=True)
            st.write(df)
            st.header("Badges 💫🌟",divider=True)
            total_badges = len(your_let_Badges["matchedUser"]["badges"])
            with st.expander(f"Total Badges: {total_badges}"):
                # Create three columns
                col1, col2, col3 = st.columns(3)

                # Iterate over badges and distribute them to columns
                for i, badge in enumerate(your_let_Badges["matchedUser"]["badges"]):
                    if i % 3 == 0:
                        with col1:
                            st.write(f"**{badge['displayName']}**")
                            st.image(badge['medal']['config']["iconGif"], width=100)
                    elif i % 3 == 1:
                        with col2:
                            st.write(f"**{badge['displayName']}**")
                            st.image(badge['medal']['config']["iconGif"], width=100)
                    else:
                        with col3:
                            st.write(f"**{badge['displayName']}**")
                            st.image(badge['medal']['config']["iconGif"], width=100)
            st.header("Graph 📊📈📉",divider=True)
            data=your_graph['matchedUser']['userCalendar']['submissionCalendar']
            data = json.loads(data)
            df = pd.DataFrame(list(data.items()), columns=['Timestamp', 'Count'])
            df['Date'] = pd.to_datetime(df['Timestamp'].astype(int), unit='s')
            df.set_index('Date', inplace=True)
            daily_counts = df['Count'].resample('D').sum().fillna(0)
            cmap = 'plasma' 
            fig, ax = calplot.calplot(daily_counts, cmap=cmap, figsize=(12, 6),colorbar=False)
            st.pyplot(fig)
        with midle:
            st.markdown("""
            <style>
            .vertical-line {
                border-left: 2px solid black;
                height: 3200px;
            }
            </style>

            <div class="vertical-line"></div>
            """, unsafe_allow_html=True)

        with friend:
            user_profile = friend_data['userProfile']
            contest_info = friend_data['userContestRanking']  
            ko=[]
            for stat in user_profile['submitStats']['acSubmissionNum']:
                ko=ko+[stat['count']]         
            cols = st.columns([1,2.9])
            with cols[0]:
                    image = st.image(user_profile['profile']['userAvatar'])
            st.markdown(
                    """
                    <style>
                    .circle-image {
                        border-radius: 50%;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                # Create a link around the image
            image_html = f'<a href="{link}" target="_blank"></a>'
            st.markdown(image_html, unsafe_allow_html=True)
            with cols[1]:
                    z=friend_data['userProfile']['username']
                    ui.metric_card(title="User Name", content=z, description="", key="card24")
            perc,ratong = st.columns([1,1])
            with perc:
                ui.metric_card(title="Top Percentage", content=contest_info['topPercentage'], description="Great🥰", key="card26")
            with ratong:
                ui.metric_card(title="Rating", content=user_profile['profile']['ranking'], description="Good😁", key="card36") 
            st.header("Easy-Medium-Hard😊😑😥", divider=True)
            total_questions = ko[0]
            easy_questions = ko[1]
            medium_questions = ko[2]
            hard_questions = ko[3]
            easy_percent = (easy_questions / total_questions) * 100
            medium_percent = (medium_questions / total_questions) * 100
            hard_percent = (hard_questions / total_questions) * 100
            col1,  col3 = st.columns([3, 1])
            with col1:
                            ui.metric_card(title="Total Question ", content=ko[0], key="card94")                        
                            fig, ax = plt.subplots()
                            ax.pie([easy_percent, medium_percent, hard_percent],
                                labels=["Easy", "Medium", "Hard"],
                                autopct="%1.1f%%",
                                startangle=140)
                            ax.axis("equal")  # Equal aspect ratio for a circular pie chart
                            st.pyplot(fig)

                      # Display difficulty counts
            with col3:
                            ui.metric_card(title="Easy ", content=ko[1], key="card124")
                            ui.metric_card(title="Medium", content=ko[2], key="card104")
                            ui.metric_card(title="Hard ", content=ko[3], key="card114")

            st.header("SkillTracker🤹‍♂️🦾", divider=True)

            categories = list(friends_df["Category"].unique())
            selected_categories = st.multiselect("Select Categories for Friends' Data", categories, default=categories, key="friends_categories")

            # Filter and Sort Data
            filtered_friends_df = friends_df[friends_df["Category"].isin(selected_categories)]
            sorted_friends_df = filtered_friends_df.sort_values(by="Problems Solved", ascending=False)

            # Bar Chart
            
            fig, ax = plt.subplots(figsize=(6, 4))
            for category in sorted_friends_df["Category"].unique():
                category_data = sorted_friends_df[sorted_friends_df["Category"] == category]
                ax.bar(category_data["Topic"], category_data["Problems Solved"], label=category)

            ax.set_ylabel("Problems Solved")
            ax.set_xlabel("Topic")
            ax.set_title("Friends' Problems Solved (Sorted)")
            ax.legend()
            plt.xticks(rotation=90, ha="right")
            st.pyplot(fig)

            # Detailed Data
            st.subheader("Detailed Data View")
            st.dataframe(sorted_friends_df)




            language_data = friend_data['matchedUser']['languageProblemCount']
            language_df = pd.DataFrame(language_data)
            language_df.columns = ["Language", "Problems Solved"]
            st.header("Questions per Language🤠", divider=True)
            st.table(language_df)

            header = [ "Question Name", "Timestamp"]
            def format_timestamp(timestamp):
                                dt_object = datetime.datetime.fromtimestamp(int(timestamp))
                                return dt_object.strftime("%Y-%m-%d %I:%M %p")  # AM/PM format
            processed_data = []
                           
                          
            for submission in friend_RQuestion:
                                formatted_date = format_timestamp(submission['timestamp'])
                                processed_data.append([ submission['title'], formatted_date])
            df = pd.DataFrame(processed_data, columns=["Question Name", "Timestamp"])
            
            st.header("Your Recent Question😊📕📅",divider=True)
            st.write(df)
            total_badges = len(friend_let_Badges["matchedUser"]["badges"])

            # Create the expander
            
            st.header("Badges 💫🌟",divider=True)
            with st.expander(f"Total Badges: {total_badges}"):
                # Create three columns
                col1, col2, col3 = st.columns(3)

                # Iterate over badges and distribute them to columns
                for i, badge in enumerate(friend_let_Badges["matchedUser"]["badges"]):
                    if i % 3 == 0:
                        with col1:
                            st.write(f"**{badge['displayName']}**")
                            st.image(badge['medal']['config']["iconGif"], width=100)
                    elif i % 3 == 1:
                        with col2:
                            st.write(f"**{badge['displayName']}**")
                            st.image(badge['medal']['config']["iconGif"], width=100)
                    else:
                        with col3:
                            st.write(f"**{badge['displayName']}**")
                            st.image(badge['medal']['config']["iconGif"], width=100)

            st.header("Graph 📊📈📉",divider=True)
            data=friend_graph['matchedUser']['userCalendar']['submissionCalendar']
            data= json.loads(data)
            df = pd.DataFrame(list(data.items()), columns=['Timestamp', 'Count'])
            
            df['Date'] = pd.to_datetime(df['Timestamp'].astype(int), unit='s')
            df.set_index('Date', inplace=True)
            daily_counts1 = df['Count'].resample('D').sum().fillna(0)
            cmap = 'plasma' 
            fig3, ax = calplot.calplot(daily_counts1, cmap=cmap, figsize=(12, 6),colorbar=False)
            st.pyplot(fig3) 
        codeforce_your=your_id[2]
        codeforce_friend=friends_id[2]
        codechef_username_your=your_id[1]
        codechef_username_friend=friends_id[1]



        with your:   
       
            st.header("Codeforces and Codechef ",divider=True)
            data=get_user_data(codeforce_your)
            # last_online_time = datetime.utcfromtimestamp(data["lastOnlineTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S')
            # registration_time = datetime.utcfromtimestamp(data["registrationTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S')
            st.image(data["avatar"], caption="User's Avatar", width=100)
            st.subheader(f"Username: {data['handle']}")

            # Display Rating and Rank
            st.write(f"**Rank:** {data['rank']}")
            st.write(f"**Max Rank:** {data['maxRank']}")
            st.write(f"**Rating:** {data['rating']}")
            st.write(f"**Max Rating:** {data['maxRating']}")

            # Display Friend Count and Contribution
            st.write(f"**Friend Count:** {data['friendOfCount']}")
            st.write(f"**Contribution:** {data['contribution']}")

            
        with midle:
            st.markdown("""
            <style>
            .vertical-line {
                border-left: 2px solid black;
                height: 1900px;
            }
            </style>

            <div class="vertical-line"></div>
            """, unsafe_allow_html=True)

        with friend:
            st.header("Codeforces and Codechef ",divider=True)

            data=get_user_data(codeforce_friend)
            # last_online_time = datetime.utcfromtimestamp(data["lastOnlineTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S')
            # registration_time = datetime.utcfromtimestamp(data["registrationTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S')
            st.image(data["avatar"], caption="User's Avatar", width=100)
            st.subheader(f"Username: {data['handle']}")

            # Display Rating and Rank
            st.write(f"**Rank:** {data['rank']}")
            st.write(f"**Max Rank:** {data['maxRank']}")
            st.write(f"**Rating:** {data['rating']}")
            st.write(f"**Max Rating:** {data['maxRating']}")

            # Display Friend Count and Contribution
            st.write(f"**Friend Count:** {data['friendOfCount']}")
            st.write(f"**Contribution:** {data['contribution']}")
       
if selected=="collage":
    ans=listofcollege(db)
    your_id = st.multiselect("which Collage ?", ans, [], placeholder="Select Your's Id")  
    
    if your_id:
        usernames=totalusers(your_id[0],4)
        user_ratings = get_ratings_for_users(usernames)
        st.write(user_ratings)
        for user, rating in user_ratings.items():
            if rating is not None:
                st.write(f"{user}'s contest rating: {rating}")
            else:
                st.write(f"Could not retrieve contest rating for {user}")
        active_days_list = get_active_days_for_users(usernames)

        if active_days_list:
            for username, days in active_days_list:
                st.write(f"{username}: {days} active days in 2024")
        else:
            st.write("Error fetching active days for some users.")


