import PyPDF2
import streamlit as st
import pandas as pd
import re
from datetime import date
import PIL.Image
from PIL import Image
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calplot
import plotly.express as px
from pathlib import Path
from streamlit_ace import st_ace
from streamlit_option_menu import option_menu
import datetime
import os
import base64
import streamlit_shadcn_ui as ui
import textwrap
import google.generativeai as genai
from IPython.display import display,Markdown
from streamlit_lottie import st_lottie
import requests 
from local_components import card_container
import sys
import io
import speech_recognition as sr
import pdf2image
import plotly.graph_objects as go
import plotly.express as px

global s
k=0
api_key=os.getenv("API-KEY")
genai.configure(api_key=os.getenv("API-KEY"))
t=[ "Python", "Java", "C++", "JavaScript", "Ruby", "PHP", "Swift", "Kotlin", 
    "C#", "Go", "R", "TypeScript", "Scala", "Perl", "Objective-C", "Dart", 
    "Rust", "Haskell", "MATLAB", "SQL", "HTML/CSS", "React", "Angular", "Vue.js", 
    "Node.js", "Django", "Flask", "Spring", "ASP.NET", "Ruby on Rails"]
EXAMPLE_NO = 1
recognizer = sr.Recognizer()
st.set_page_config(page_title="KnowledgeBuilder", page_icon='src/Logo College.png', layout="wide", initial_sidebar_state="auto", menu_items=None)
if "current_theme" not in st.session_state:
    st.session_state.current_theme = "light"
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
def get_leetcode_data(username):
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
      recentAcSubmissionList(username: $username, limit: 15) {
            id
            title
            titleSlug
            timestamp
          }
     
    }
    
    """
    variables = {
        "username": username
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    if 'errors' in data:
        print("Error:", data['errors'])
        return None

    return data['data']
def get_gemini_response1(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text
def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json() 
def streamlit_menu(example=1):
    if example == 1:
        with st.sidebar:
            selected = option_menu(
                menu_title="Profile - Builder ",  # required
                options=["Dashboard", "ATS Detector", "LinkedIn Profile","Your Progress"],  # required
                icons=["bi bi-person-lines-fill", "bi bi-binoculars-fill", "bi bi-linkedin","bi bi-envelope-at"],  # optional
                menu_icon="cast",  # optional
                 
                default_index=0,
            )
        return selected
def create_rating_dropdown(label):
    return st.selectbox(label, ['1', '2', '3', '4', '5'], index=2)
selected = streamlit_menu(example=EXAMPLE_NO)

if 'questions' not in st.session_state:
    st.session_state.questions = []
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
                    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
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
                "IT Project Manager"
            ]
            selected_role = st.selectbox("Select your job role", job_roles)

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
if selected == "Your Progress":
            link="https://lottie.host/c2f561ff-c620-47ef-81ae-1c2316627a6f/KnRJZhxv5D.json"
            l=load_lottieurl(link)
            col1, col2 = st.columns([1.3,9])  # Create two columns
            with col1:
                st.lottie(l, height=100, width=100)
            with col2:
                st.header(f":rainbow[Mails/Coverletter]", divider='rainbow')
                
            
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                if st.button("Cover Letters"):
                    pass
            with col2:
                if st.button("Referrals"):
                    pass
            with col3:
                if st.button("Mails"):
                    pass
            with col4:
                if st.button("Button 4"):
                    pass
            with col5:
                if st.button("Button 5"):
                    pass


                    
