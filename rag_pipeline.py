from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from transformers import pipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

_LOCAL_LLM = None
_LOCAL_EMBEDDINGS = None

def get_llm_and_embeddings():
    """Returns local HuggingFace LLM and Embeddings, no API keys needed."""
    global _LOCAL_LLM, _LOCAL_EMBEDDINGS
    
    if _LOCAL_EMBEDDINGS is None:
        # Fast, small local embeddings model
        _LOCAL_EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
    if _LOCAL_LLM is None:
        # Small LLM that can run locally on CPU/GPU without API keys
        # flan-t5-small is relatively small and fast
        hf_pipeline = pipeline(
            "text2text-generation", 
            model="google/flan-t5-small", 
            max_new_tokens=150
        )
        _LOCAL_LLM = HuggingFacePipeline(pipeline=hf_pipeline)
        
    return _LOCAL_LLM, _LOCAL_EMBEDDINGS

def build_vector_store(df):
    """
    Converts a Pandas DataFrame to LangChain Documents and 
    builds a Chroma vector database for similarity search.
    """
    documents = []
    for index, row in df.iterrows():
        row_str = " | ".join([f"{col}: {val}" for col, val in row.items()])
        doc = Document(page_content=row_str, metadata={"row_index": index})
        documents.append(doc)
    
    _, embeddings = get_llm_and_embeddings()
    
    # Create Chroma vector store
    vectorstore = Chroma.from_documents(documents, embedding=embeddings, persist_directory="./chroma_db")
    return vectorstore

def answer_query(vectorstore, query):
    """
    Runs similarity search to get relevant context and passes it to the local LLM.
    """
    llm, _ = get_llm_and_embeddings()
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    template = """You are a helpful Data Analyst Assistant. 
Use the following pieces of retrieved context from a spreadsheet to answer the question. 
If you don't know the answer based on the context, just say that you don't know. 
Keep your answer analytical and clear. Include context where necessary.

Context:
{context}

Question:
{question}

Answer:"""
    
    prompt = PromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n".join(doc.page_content for doc in docs)
        
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain.invoke(query)
