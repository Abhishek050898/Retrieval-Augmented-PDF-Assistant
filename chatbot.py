from langchain.tools import DuckDuckGoSearchRun
import google.generativeai as genai
from config import GEMINI_API_KEY

# ✅ Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Web Search Fallback
search_tool = DuckDuckGoSearchRun()

def qa_bot(query, vector_store):
    """Retrieves answer from FAISS, falls back to web search if necessary."""
    
    # ✅ Try FAISS Retrieval
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    retrieved_docs = retriever.get_relevant_documents(query)
    
    use_faiss = False  # Track if FAISS should be used

    if retrieved_docs:
        faiss_context = "\n".join([doc.page_content for doc in retrieved_docs]).strip()

        # ✅ Ensure FAISS does not give a "not found" message
        if "does not mention" in faiss_context.lower() or "i cannot answer" in faiss_context.lower():
            print("⚠️ FAISS returned an irrelevant response. Ignoring it.")
        else:
            use_faiss = True  # FAISS contains useful data

    # ✅ Web Search Fallback
    if not use_faiss:
        print("🔍 FAISS failed. Performing web search...")
        search_results = search_tool.run(query).strip()

        if search_results:
            context = search_results  # Use web search results
            source = "Web Search"
        else:
            return "❌ No relevant answer found in the PDF or online sources."
    
    else:
        context = faiss_context  # Use FAISS results
        source = "FAISS Database"

    # try:
        # ✅ Generate response using Google Gemini API
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Context: {context}\nQuestion: {query}")
        return response.text
        
        # if response and response.text.strip():
        #     return f"✅ Answer from {source}: {response.text}"
        # else:
        #     return "❌ No meaningful response generated."

    # except Exception as e:
    #     return f"⚠️ Error generating response: {str(e)}"
