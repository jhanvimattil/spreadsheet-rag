import streamlit as st
import os
from dotenv import load_dotenv
from file_loader import load_and_clean_file_data
from rag_pipeline import build_vector_store, answer_query

load_dotenv()

st.set_page_config(page_title="Data Analyst Assistant", layout="wide")

st.title("📊 Data Analyst Assistant")
st.write("Upload a CSV or Excel file and ask questions about your data.")



# Main area
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=['csv', 'xls', 'xlsx'])

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if st.button("Ingest Data"):
    if not uploaded_file:
        st.error("Please upload a file first.")
    else:
        with st.spinner("Reading and cleaning data..."):
            try:
                df = load_and_clean_file_data(uploaded_file)
                st.success(f"Data loaded successfully! ({len(df)} rows, {len(df.columns)} columns)")
                st.dataframe(df.head()) # show preview
                
                with st.spinner("Building vector database..."):
                    vectorstore = build_vector_store(df)
                    st.session_state.vectorstore = vectorstore
                    st.success("Vector database built successfully. You can now ask questions!")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

# Chat interface
st.subheader("💬 Ask Questions")
query = st.text_input("What would you like to know about the data?")

if st.button("Ask"):
    if not st.session_state.vectorstore:
        st.warning("Please upload and ingest a file first.")
    elif not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing data and generating answer..."):
            try:
                answer = answer_query(st.session_state.vectorstore, query)
                st.markdown("### Answer")
                st.info(answer)
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
