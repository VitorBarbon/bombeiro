import pandas as pd
from typing import Tuple, List, Dict, Any

def extract_data_from_xlsx(file_path: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    # Read the Excel file
    data = pd.ExcelFile(file_path)
    
    # Extract data from the 'client' sheet
    df_client = pd.read_excel(data, sheet_name='client')
    data_client = df_client.to_dict(orient='records')
    
    # Extract data from the 'participants' sheet
    df_participants = pd.read_excel(data, sheet_name='participants')
    data_participants = df_participants.to_dict(orient='records')
    
    return data_client, data_participants
