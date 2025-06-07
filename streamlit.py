# streamlit_app.py

import streamlit as st
import requests
import pandas as pd
import re

def parse_cited_chunks(chunk_list):
    rows = []
    pattern = r"(.+?) \(Page (\d+), Para (\d+)\) — (.+)"

    for chunk in chunk_list:
        match = re.match(pattern, chunk)
        if match:
            doc_id, page, para, summary = match.groups()
            rows.append({
                "Doc ID": doc_id.strip(),
                "Page": int(page),
                "Paragraph": int(para),
                "Summary": summary.strip()
            })
        else:
            rows.append({
                "Doc ID": "Unknown",
                "Page": "-",
                "Paragraph": "-",
                "Summary": chunk
            })
    return pd.DataFrame(rows)

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Wasserstoff Gen-AI", layout="centered")

st.title("📚 Wasserstoff Theme Identifier")
st.markdown("Upload legal PDFs and ask questions to extract themes from them.")

# ---- Upload Section ----
st.subheader("Upload Document")
uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Uploading and processing..."):
        response = requests.post(
            f"{API_URL}/upload",
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )
    if response.status_code == 200:
        st.success("✅ File uploaded and processed!")
    else:
        st.error("❌ Upload failed")

# ---- Query Section ----
st.subheader("Ask a Question")

question = st.text_input("Type your legal query here...")

if st.button("Get Themes"):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing documents..."):
            res = requests.post(f"{API_URL}/themes", json={"question": question})

        if res.status_code == 200:
            data = res.json()

            st.markdown("### 🧠 Theme Summary")
            st.code(data['theme_summary'], language="text")

            st.markdown("### 🧾 Raw Answers (Cited Chunks)")
            df = parse_cited_chunks(data["raw_answers"])
            st.dataframe(df, use_container_width=True)



        else:
            st.error("⚠️ Error: Unable to process query.")
