import streamlit as st
import os
from dotenv import load_dotenv


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

# Main Chat
st.set_page_config(page_title="PDF Chat - Groq RAG", page_icon="📄", layout="wide")
st.title("📄 Chat with your PDF (Groq RAG)")


if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chain" not in st.session_state:
    st.session_state.chain = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file and st.button("Process PDF"):
        with st.spinner("Processing PDF... This may take a minute for large files"):
            # Save uploaded file temporarily
            temp_path = "temp_uploaded.pdf"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 1. Load PDF
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            
            # 2. Split into chunks (good for 10MB PDFs)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(docs)
            
            # 3. Embeddings + Vector Store
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = FAISS.from_documents(chunks, embeddings)
            
            st.session_state.vectorstore = vectorstore
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            st.success(f"✅ PDF processed! {len(chunks)} chunks created.")

    st.divider()
    st.info("**Tips:**\n"
            "- Works best with text-heavy PDFs\n"
            "- Groq free tier: ~1000 requests/day on 70B model\n"
            "- Large PDFs may take 30-90 seconds to process")

# ====================== MAIN CHAT ======================
if st.session_state.vectorstore is None:
    st.info("👈 Please upload and process a PDF from the sidebar to start chatting.")
else:
    # Initialize LLM and Chain (only once)

    if st.session_state.chain is None:
        
        # Force reload .env and get key
        load_dotenv(override=True)          # ← important on Windows
        groq_key = os.getenv("GROQ_API_KEY")
        
        if not groq_key:
            st.error("❌ GROQ_API_KEY is missing!\n\n"
                     "1. Create a file named exactly `.env` (with the dot) in the same folder as app.py\n"
                     "2. Put this inside it:\n"
                     "   GROQ_API_KEY=gsk_your_actual_key_here\n"
                     "3. Save and restart Streamlit (Ctrl+C then run again)")
            st.stop()   # stops the app from crashing
        
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1024,
            api_key=groq_key          # ← THIS IS THE FIX
        )
        
        retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 4})
        
        template = """You are a helpful assistant. Answer the question based **only** on the following context from the PDF.
If the answer is not in the context, say: "I don't have enough information in the document to answer this."

Context:
{context}

Question: {question}
Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        st.session_state.chain = chain
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the PDF..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chain.invoke(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "rate limit" in error_msg.lower():
                        st.error("⚠️ Groq daily limit reached. Please try again tomorrow or use a different key.")
                    else:
                        st.error(f"Error: {error_msg}")

# Footer
st.caption("Built with LangChain + Groq + FAISS | Free tier friendly")