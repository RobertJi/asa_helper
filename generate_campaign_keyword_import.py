import csv
import os
from typing import List, Dict

def read_keyword_export(filepath: str) -> List[Dict]:
    """
    Read and parse the keyword export CSV file.
    Only returns active keywords with their relevant details.
    """
    keywords = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if keyword status is "ACTIVE" - note the exact column names
                if row.get('Status', '') == 'ACTIVE':
                    keywords.append({
                        'keyword': row['Keyword'],
                        'match_type': row['Match Type'],  # Changed from 'Match type'
                        'ad_group': row['Ad Group ID']    # Changed from 'Ad group'
                    })
    except Exception as e:
        print(f"Error reading file {filepath}: {str(e)}")
        return []
    
    print(f"Found {len(keywords)} active keywords")
    return keywords

def generate_import_csv(keywords: List[Dict], output_path: str, campaign_name: str, 
                       campaign_id: int, ad_group_id: int, default_bid: float, match_type: str) -> bool:
    """
    Generate a CSV file for importing keywords to a new campaign.
    
    CSV Format:
    Action,Keyword ID,Keyword,Match Type,Status,Bid,Campaign ID,Ad Group ID
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            
            # Write header matching exact CSV format
            writer.writerow(['Action', 'Keyword ID', 'Keyword', 'Match Type', 'Status', 
                           'Bid', 'Campaign ID', 'Ad Group ID'])
            
            # Write keyword data
            for kw in keywords:
                writer.writerow([
                    'CREATE',           # Action
                    '',                 # Keyword ID (empty for new keywords)
                    kw['keyword'],      # Keyword
                    match_type,   # Match Type
                    'ACTIVE',           # Status
                    f"{default_bid:.2f}", # Bid
                    campaign_id,        # Campaign ID
                    ad_group_id         # Ad Group ID
                ])
        
        print(f"Successfully generated import file at {output_path}")
        print(f"Total keywords written: {len(keywords)}")
        return True
    
    except Exception as e:
        print(f"Error generating import file: {str(e)}")
        return False

def main():
    # Configuration
    INPUT_FILE = "output/campaign_1726069162_adgroup_1726011485_keyword_import.csv"
    
    # Define campaign and ad group IDs
    NEW_CAMPAIGN_ID = 1726069162
    NEW_AD_GROUP_ID = 1725976928
    
    # Generate output filename with campaign and ad group IDs
    OUTPUT_FILE = f"output/campaign_{NEW_CAMPAIGN_ID}_adgroup_{NEW_AD_GROUP_ID}_keyword_import.csv"
    NEW_CAMPAIGN_NAME = "New Campaign"  # Change this to your desired campaign name
    DEFAULT_BID = 0.30  # Change this to your desired default bid
    MATCH_TYPE = 'BROAD'

    # Read active keywords from export file
    keywords = read_keyword_export(INPUT_FILE)
    
    if not keywords:
        print("No active keywords found or error reading input file")
        return
    
    # Generate import file
    generate_import_csv(
        keywords=keywords,
        output_path=OUTPUT_FILE,
        campaign_name=NEW_CAMPAIGN_NAME,
        campaign_id=NEW_CAMPAIGN_ID,
        ad_group_id=NEW_AD_GROUP_ID,
        default_bid=DEFAULT_BID,
        match_type=MATCH_TYPE
    )

if __name__ == "__main__":
    main()