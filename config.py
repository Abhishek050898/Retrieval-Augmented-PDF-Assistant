import streamlit as st

# ✅ Correct way to access OpenAI API key
OPENAI_API_KEY = st.secrets["secrets"]["openai_api_key"]
GEMINI_API_KEY = st.secrets["secrets"]["gemini_api_key"]

# ✅ FAISS Storage Path
DB_FAISS_PATH = "vectorstores/db_faiss"
MODEL_NAME = "gemini-pro"  


#st.write(f"🔍 Using OpenAI Model: {MODEL_NAME}")
