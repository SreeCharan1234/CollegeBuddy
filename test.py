# import os
# from phi.agent import Agent, RunResponse
from phi.model.google import Gemini

# # Set your API key here
# os.environ["GOOGLE_API_KEY"] = ""

# agent = Agent(
#     model=Gemini(id="gemini-1.5-flash"),
#     markdown=True,
# )

# # Print the response in the terminal
# agent.print_response("Share a 2 sentence horror story.")

#impimettation of groq api key  now going with 
# import os

# from groq import Groq

# client = Groq(
#     api_key="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",
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama-3.3-70b-versatile",
# )

# print(chat_completion.choices[0].message.content)
from phi.agent import Agent

agent = Agent(
    description="You are a famous short story writer asked to write for a magazine",
    instructions=["You are a pilot on a plane flying from Hawaii to Japan."],
    markdown=True,
    debug_mode=True,
)
agent.print_response("Tell me a 2 sentence horror story.", stream=True)