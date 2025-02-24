import streamlit as st
from pdf_processor import process_uploaded_pdf
from chatbot import qa_bot


if "vector_store" not in st.session_state:
    st.session_state.vector_store = None


if "conversation" not in st.session_state:
    st.session_state.conversation = []

def main():
    st.set_page_config(page_title="PDF Assistant")

    # 🔹 Sidebar (PDF Upload)
    with st.sidebar:
        st.title('PDF Assistant 🚀🤖')
        uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

        if uploaded_file is not None:
            with st.spinner("Processing PDF..."):
                st.session_state.vector_store = process_uploaded_pdf(uploaded_file)
            st.success("✅ PDF Processed! You can start chatting.")

        if st.button("Clear Chat"):
            st.session_state.conversation = []
            st.session_state.vector_store = None

            
    # 🔹 Main Chat UI
    st.title("PDF Assistant")
    # Custom CSS for styling chat bubbles
    st.markdown(
    """
    <style>
        /* Increase font size for the entire UI */
        html, body, [class*="st-"] {
            font-size: 18px !important;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
            height: 400px;
            overflow-y: auto;
            padding: 10px;
        }

        .user-bubble {
            background-color: #007bff;
            color: white;
            align-self: flex-end;
            border-radius: 10px;
            padding: 10px;
            margin: 5px;
            max-width: 70%;
            word-wrap: break-word;
            font-size: 20px; /* Increased font size */
        }

        .bot-bubble {
            background-color: #f1f1f1;
            color: black;
            align-self: flex-start;
            border-radius: 10px;
            padding: 10px;
            margin: 5px;
            max-width: 70%;
            word-wrap: break-word;
            font-size: 20px; /* Increased font size */
        }

        /* Increase font size of input fields */
        input, textarea {
            font-size: 18px !important;
        }

        /* Increase button text size */
        button {
            font-size: 18px !important;
        }

        /* Increase text size for sidebar */
        .stSidebar {
            font-size: 18px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

    query = st.text_input("Ask your question:", placeholder="Type your question here...")

    if st.button("Get Answer"):
        if query:
            if st.session_state.vector_store is None:
                st.warning("Please upload a PDF first.")
            else:
                with st.spinner("Processing..."):
                    st.session_state.conversation.append({"role": "user", "message": query})
                    answer = qa_bot(query, st.session_state.vector_store)
                    st.session_state.conversation.append({"role": "bot", "message": answer})

        else:
            st.warning("Please enter a question.")

    # 🔹 Display Chat History
    chat_container = st.empty()
    chat_bubbles = ''.join(
        [f'<div class="{c["role"]}-bubble">{c["message"]}</div>' for c in st.session_state.conversation]
    )
    chat_container.markdown(f'<div class="chat-container">{chat_bubbles}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
