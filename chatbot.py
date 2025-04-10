import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate 
from langchain_core.prompts import ChatPromptTemplate 

import requests
try:
    response = requests.get("http://localhost:11434/")
    print(response.status_code)
except requests.exceptions.RequestException as e:
    print("Error connecting to the server:", e)


st.title(" Gender Based Queries Chatbot")
st.write("Made by Parth Awasthi, Solution Developer Intern, I-Tech Mission")

model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434/")

system_message = SystemMessagePromptTemplate.from_template("You are an AI assistant focused on providing up-to-date, evidence-based information"
    "about gender equality, gender-based violence prevention, economic empowerment of women, "
    "political participation, health and reproductive rights, and education. "
    "Provide well-researched responses, citing best practices and policies when possible.")

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []
    
with st.form("llm-form"):
    text = st.text_area("Enter your questions here:")
    submit = st.form_submit_button("Submit")
    
def generate_response(chat_history):
    chat_template = ChatPromptTemplate.from_messages(chat_history)
    
    chain = chat_template | model | StrOutputParser()
    
    response = chain.invoke({})
    
    return response

#if user message in 'user' key
# ai message in 'assistant' key 
def get_history():
    chat_history = [system_message]
    for chat in st.session_state['chat_history']:
        
        prompt = HumanMessagePromptTemplate.from_template(chat['user'])
        chat_history.append(prompt)
        
        ai_message = AIMessagePromptTemplate.from_template(chat['assistant'])
        chat_history.append(ai_message)
        
    return chat_history


if submit and text:
    with st.spinner("Generating response..."):
        prompt = HumanMessagePromptTemplate.from_template(text)
        
        chat_history = get_history()
        
        chat_history.append(prompt)
        
        response = generate_response(chat_history)
        
        st.session_state['chat_history'].append({"user": text, "assistant": response})
        
st.write('## Chat History')
for chat in reversed(st.session_state['chat_history']):
    st.write(f"**User:** {chat['user']}")
    st.write(f"**Assistant:** {chat['assistant']}")