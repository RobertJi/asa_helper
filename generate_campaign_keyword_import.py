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
                # Check if keyword is active (enabled/on)
                if row.get('Status', '').lower() == 'enabled':
                    keywords.append({
                        'keyword': row['Keyword'],
                        'match_type': row['Match type'],
                        'ad_group': row['Ad group']
                    })
    except Exception as e:
        print(f"Error reading file {filepath}: {str(e)}")
        return []
    
    print(f"Found {len(keywords)} active keywords")
    return keywords


def generate_import_csv(keywords: List[Dict], output_path: str, campaign_name: str, default_bid: float) -> bool:
    """
    Generate a CSV file for importing keywords to a new campaign.
    
    CSV Format:
    Campaign,Ad group,Keyword,Match type,Bid
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            
            # Write header
            writer.writerow(['Campaign', 'Ad group', 'Keyword', 'Match type', 'Bid'])
            
            # Write keyword data
            for kw in keywords:
                writer.writerow([
                    campaign_name,
                    kw['ad_group'],
                    kw['keyword'],
                    kw['match_type'],
                    f"{default_bid:.2f}"
                ])
        
        print(f"Successfully generated import file at {output_path}")
        print(f"Total keywords written: {len(keywords)}")
        return True
    
    except Exception as e:
        print(f"Error generating import file: {str(e)}")
        return False


def main():
    # Configuration
    INPUT_FILE = "input/ad_group_keyword_list.csv"
    OUTPUT_FILE = "output/campaign_keyword_import.csv"
    NEW_CAMPAIGN_NAME = "New Campaign"  # Change this to your desired campaign name
    DEFAULT_BID = 0.50  # Change this to your desired default bid
    
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
        default_bid=DEFAULT_BID
    )


if __name__ == "__main__":
    main() 