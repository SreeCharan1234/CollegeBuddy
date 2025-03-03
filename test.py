import time
import google.generativeai as genai

#Store the last time the api was called.
last_api_call = 0
def get_gemini_response(question):
    global last_api_call
    current_time = time.time()
    if current_time - last_api_call < 1: #1 second delay.
        time.sleep(1 - (current_time - last_api_call))
    model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')
    response = model.generate_content(question)
    last_api_call = time.time()
    return response.text
get_gemini_response("What is the capital of India?")