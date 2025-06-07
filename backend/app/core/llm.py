from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv
load_dotenv(dotenv_path="C:/Users/Aryan Sharma/OneDrive/Desktop/task2/chatbot_theme_identifier/backend/app/core/.env")
api_key=os.environ.get("GROQ_API_KEY")
def query_llm ( question : str , context:str)->str:
    model = ChatGroq(temperature=0,model="gemma2-9b-it",api_key=api_key)
    prompt = f"""You are a helpful AI assistant. 
    Use the following context to answer the question. Be specific and cite doc_id, page, and paragraph when relevant.

    Context:
    {context}

    Question:
    {question}
    """
    response = model.invoke(prompt)
    return response.content