# Data Analyst Assistant
A simple, fully local Retrieval-Augmented Generation (RAG) application that allows you to upload a CSV or Excel dataset and ask questions about it using AI.
## Features
- **100% Local & Offline**: Uses HuggingFace transformers (`flan-t5-small` for the LLM and `all-MiniLM-L6-v2` for embeddings). No API keys (like OpenAI or Google Gemini) are required, meaning your data never leaves your machine.
- **Easy File Uploads**: Drag and drop `.csv` or `.xlsx` files directly into the web interface.
- **Automated Data Cleaning**: Automatically cleans the dataset (e.g., removing entirely empty rows/columns, standardizing headers) before processing.
- **Vector Database**: Uses ChromaDB to store and retrieve the most relevant rows for your questions.
- **Interactive UI**: Built with Streamlit for a clean, easy-to-use chat interface.
## Prerequisites
- Python 3.9+
- macOS / Linux / Windows
## Installation
1. **Clone or download this repository** to your local machine.
2. **Navigate to the project directory**:
   ```bash
   cd da-assist
   ```
3. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The first time you run this, it will download PyTorch and Transformers which might take a few minutes depending on your internet connection).*
## Usage
1. **Start the application**:
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```
2. **Open your browser** and navigate to `http://localhost:8501`.
3. **Upload your dataset** using the file uploader and click **Ingest Data**.
   > **Note:** The very first time you ingest data or ask a question, the application will download the local AI models (~500MB total) into your HuggingFace cache. Subsequent runs will be completely offline and much faster.
4. **Ask Questions!** Type your query in the chat box at the bottom (e.g., *"What is the average of the sales column?"*) to get an AI-generated answer based on your data.
## Project Structure
- `app.py`: The main Streamlit web interface.
- `file_loader.py`: Handles reading and cleaning uploaded CSV/Excel files using Pandas.
- `rag_pipeline.py`: Manages the local LLM, embeddings, and ChromaDB vector store.
- `requirements.txt`: Python dependencies.
