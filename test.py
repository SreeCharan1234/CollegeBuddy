import os
from langchain_huggingface import HuggingFaceEndpoint
sec_key="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"
os.environ["HUGGINGFACEHUB_API_TOKEN"]=sec_key
repo_id="mistralai/Mistral-7B-Instruct-v0.2"
llm=HuggingFaceEndpoint(repo_id=repo_id,temperature=0.7,token=sec_key)
print(llm.invoke(s))
