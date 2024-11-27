import pandas as pd
import os
from typing import Optional


def csv_to_xlsx(csv_path: str, xlsx_path: Optional[str] = None) -> bool:
    """
    Convert a CSV file to XLSX format.
    
    Args:
        csv_path: Path to the input CSV file
        xlsx_path: Path for the output XLSX file. If None, will use same path as CSV but with .xlsx extension
        
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        if not xlsx_path:
            # Replace .csv with .xlsx in the original path
            xlsx_path = os.path.splitext(csv_path)[0] + '.xlsx'
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(xlsx_path), exist_ok=True)
        
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Write to XLSX
        df.to_excel(xlsx_path, index=False)
        
        print(f"Successfully converted CSV to XLSX: {xlsx_path}")
        return True
        
    except Exception as e:
        print(f"Error converting CSV to XLSX: {str(e)}")
        return False 