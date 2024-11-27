import pandas as pd
import os
from util.openai_util import extract_keywords_from_diandian
from util.csv_util import csv_to_xlsx


def generate_keyword_import_file():
    # Define constants
    CAMPAIGN_ID = 1120711183
    AD_GROUP_ID = 1120771408
    MATCH_TYPE = 'EXACT'
    BID = 1.0
    INPUT_FILE = 'input/联想词列表.txt'
    ACTIVE_STATUS = 'ACTIVE'

    try:
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Read the input file
        with open(INPUT_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse keywords using OpenAI
        print("Parsing keywords from input file...")
        keywords = extract_keywords_from_diandian(content)
        
        if not keywords:
            print("No valid keywords found in input file")
            return
            
        print(f"Found {len(keywords)} keywords")
        
        # Prepare data for output
        output_data = []
        for keyword in keywords:
            output_data.append({
                'Action': 'CREATE',
                'Keyword ID': '',
                'Keyword': keyword,
                'Match Type': MATCH_TYPE,
                'Status': ACTIVE_STATUS,
                'Bid': BID,
                'Campaign ID': CAMPAIGN_ID,
                'Ad Group ID': AD_GROUP_ID
            })
        
        # Create DataFrame
        output_df = pd.DataFrame(output_data)
        
        # Export to CSV
        output_file = f"output/{CAMPAIGN_ID}_{AD_GROUP_ID}_suggested_keyword_import.csv"
        output_df.to_csv(output_file, index=False, na_rep='')
        
        print(f"Successfully generated keyword import files:")
        print(f"CSV: {output_file}")
        print(f"XLSX: {os.path.splitext(output_file)[0] + '.xlsx'}")
        print(f"Total keywords processed: {len(keywords)}")
        
    except Exception as e:
        print(f"Error generating import file: {str(e)}")


if __name__ == "__main__":
    generate_keyword_import_file() 