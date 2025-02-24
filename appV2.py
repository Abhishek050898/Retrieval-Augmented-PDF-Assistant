import streamlit as st
from pdf_processor import process_uploaded_pdf
from chatbot import qa_bot

# Session State Setup
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "conversation" not in st.session_state:
    st.session_state.conversation = []

def main():
    st.set_page_config(page_title="PDF Assistant", layout="wide")

    # 🔹 Sidebar (PDF Upload)
    with st.sidebar:
        st.title('📄 PDF Assistant 🚀')
        uploaded_file = st.file_uploader("📂 Upload a PDF", type=["pdf"])

        if uploaded_file is not None:
            with st.spinner("⏳ Processing PDF..."):
                st.session_state.vector_store = process_uploaded_pdf(uploaded_file)
            st.success("✅ PDF Processed! Start chatting.")

        if st.button("🗑 Clear Chat"):
            st.session_state.conversation = []
            st.session_state.vector_store = None

    # 🔹 Main Chat UI
    st.title("💬 PDF Assistant")
    
    # 🔹 Custom CSS for Styling
    st.markdown(
        """
        <style>
            /* Global UI Enhancements */
            html, body, [class*="st-"] {
                font-size: 18px !important;
                font-family: Arial, sans-serif;
            }
            
            /* Chat Container */
            .chat-container {
                display: flex;
                flex-direction: column;
                height: 600px;
                overflow-y: auto;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #ddd;
                background: #f9f9f9;
            }

            /* User Chat Bubble */
            .user-bubble {
                background-color: #007bff;
                color: white;
                align-self: flex-end;
                border-radius: 15px;
                padding: 12px;
                margin: 5px;
                max-width: 70%;
                word-wrap: break-word;
                font-size: 20px;
                box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
            }

            /* Bot Chat Bubble */
            .bot-bubble {
                background-color: #f1f1f1;
                color: black;
                align-self: flex-start;
                border-radius: 15px;
                padding: 12px;
                margin: 5px;
                max-width: 70%;
                word-wrap: break-word;
                font-size: 20px;
                box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            }

            /* Improved Text Input */
            input, textarea {
                font-size: 18px !important;
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }

            /* Button Styles */
            button {
                font-size: 18px !important;
                padding: 10px 15px;
                border-radius: 8px;
                background-color: #007bff;
                color: white;
                font-weight: bold;
                transition: 0.3s ease-in-out;
            }
            button:hover {
                background-color: #0056b3;
            }

            /* Sidebar */
            .stSidebar {
                font-size: 18px !important;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # 🔹 Sticky Chat Input
    query = st.text_input("Ask your question:", placeholder="Type your question here...")

    # 🔹 Get Answer Button
    if st.button("💡 Get Answer"):
        if query:
            if st.session_state.vector_store is None:
                st.warning("⚠ Please upload a PDF first.")
            else:
                with st.spinner("🤖 Thinking..."):
                    st.session_state.conversation.append({"role": "user", "message": query})
                    answer = qa_bot(query, st.session_state.vector_store)
                    st.session_state.conversation.append({"role": "bot", "message": answer})
        else:
            st.warning("⚠ Please enter a question.")

    # 🔹 Auto-scroll & Display Chat History
    chat_container = st.empty()
    chat_bubbles = ''.join(
        [f'<div class="{c["role"]}-bubble">{c["message"]}</div>' for c in st.session_state.conversation]
    )
    chat_container.markdown(f'<div class="chat-container">{chat_bubbles}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()