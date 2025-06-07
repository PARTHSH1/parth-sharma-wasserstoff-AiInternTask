# backend/app/core/theme_extraction.py

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="C:/Users/Aryan Sharma/OneDrive/Desktop/task2/chatbot_theme_identifier/backend/app/core/.env")
api_key=os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model_name="gemma2-9b-it", temperature=0,api_key=api_key)

def extract_themes_from_answers(answers: list) -> str:
    prompt = f"""
You are an AI assistant specialized in legal and technical document analysis. Your job is to analyze document-level answers to a user query and identify common themes.

Instructions:
1. Read all the document-level answers below.
2. Group them into 2-3 major **themes**.
3. For each theme:
   - Give a **clear, chat-style summary**.
   - Mention **which documents support the theme**, citing document ID, page number, and paragraph number.
   - Write like you're explaining to a human, not as bullet points.

Input:
{chr(10).join(answers)}

Output format:
🔹 Theme 1 -[Short Title]
Summary of the theme in 2-3 sentences. Mention key points, reasoning, or patterns.
Supported by: DOC001 (Page 2, Para 1), DOC003 (Page 4, Para 2)

🔹 Theme 2 - [Short Title]
Summary of the theme in 2-3 sentences...
Supported by: DOC002 (Page 1, Para 3), DOC004 (Page 3, Para 2)
Example:
DOC001: Talks about delay in disclosure under SEBI Clause 49.
DOC002: Mentions SEBI non-compliance.
DOC003: Talks about penalties under Company Act.

"""


    response = llm.invoke(prompt)
    return response.content[0][0]
def analyze_chunk(doc_id: str, page: int, para: int, content: str) -> str:
    prompt = f"""
You are a legal assistant. Summarize this document chunk in one short line.
Mention what the chunk is about (e.g., SEBI violation, penalty, disclosure delay, etc).

Content:
{content}
"""
    summary = llm.invoke(prompt)
    return f"{doc_id} (Page {page}, Para {para}): {summary}"
def analyze_chunk(doc_id: str, page: int, para: int, content: str) -> str:
    prompt = f"""
Summarize this legal chunk in one line. Focus on what issue is discussed (e.g., SEBI Clause 49, disclosure delay, penalty under Section 15, etc).

Content:
{content}
"""
    result = llm.predict(prompt).strip()  # ✅ only the string!
    return f"📄 **{doc_id}** (Page {page}, Para {para}) — {result}"
