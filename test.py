import google.generativeai as genai

genai.configure(api_key="AIzaSyCeFz8T7OhEY-aIHMsrMd2z-0h-cUPOybM")

for model in genai.list_models():
    print(model)