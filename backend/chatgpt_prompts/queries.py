from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain

import json
import openai
# Read the configuration file

def welcome_message():

    with open('/Users/Gabriela/Desktop/github/website_dashboards/backend/chatgpt_prompts/config.json') as f:
        config = json.load(f)
    # Get the API key from the configuration
    api_key = config['OPENAI_API_KEY']
    # Set up the OpenAI API client
    openai.api_key = api_key

    template = ChatPromptTemplate.from_messages([
        ('system', """You are a helpful assistant for an Edtech company called Edpuzzle. The company's pet is a Badger, so you are an AI assistant personified as 
        a Badger. Basically you need to guide the teacher in generating a report of one student to send to his/her parents. The report is mainly about the grades in 
         his assignments, and any information about grades the student still have open and close soon."""),
        ('human','{question}'),])

    model = ChatOpenAI(api_key=api_key, max_tokens=100)

    @chain
    def chatbot(values):
        prompt = template.invoke(values)
        return model.invoke(prompt)

    response = chatbot.invoke({"question": "How would you greet the teacher and tell your capabilities?"})

    return response

def create_report():
    
    with open('/Users/Gabriela/Desktop/github/website_dashboards/backend/chatgpt_prompts/config.json') as f:
        config = json.load(f)
    # Get the API key from the configuration
    api_key = config['OPENAI_API_KEY']
    # Set up the OpenAI API client
    openai.api_key = api_key

    template = ChatPromptTemplate.from_messages([
    ('system', """You are a helpful assistant for an Edtech company called Edpuzzle. The company's pet is a Badger, so you are an AI assistant personified as 
    a Badger. The teacher is in a page where he wants to select one student in her/his classroom to generate a summary of the assignments the student has completed,
     the grade, the assignments that still open, and similar information."""),
    ('human','{question}'),])

    model = ChatOpenAI(api_key=api_key, max_tokens=100)

    @chain
    def chatbot(values):
        prompt = template.invoke(values)
        return model.invoke(prompt)

    response = chatbot.invoke({"question": "How would you tell to the parent?"})

    return response