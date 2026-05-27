import pandas as pd
import io

def load_and_clean_file_data(uploaded_file):
    """
    Reads an uploaded CSV or Excel file and provides basic data cleaning.
    """
    try:
        # Check file extension to determine how to read it
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
            
        if df.empty:
            raise ValueError("The uploaded file is empty.")
            
        # Data Cleaning
        # Strip whitespace from column names if they are strings
        df.columns = [str(col).strip() for col in df.columns]
        
        # Drop completely empty rows and columns
        df.dropna(how='all', inplace=True)
        df.dropna(axis=1, how='all', inplace=True)
        
        # Fill NaN with empty string
        df.fillna("", inplace=True)
        
        return df

    except Exception as e:
        raise RuntimeError(f"Error reading file: {str(e)}")
