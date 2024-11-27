import pandas as pd
import os
from util.openai_util import translate_text


def generate_asa_import_file():
	# Define constants
	CAMPAIGN_ID = 1718142639
	AD_GROUP_ID = 1718512513
	MATCH_TYPE = 'BROAD'
	INPUT_FILE = 'input/coin_us_broad.csv'
	BID = 0.2
	TARGET_LANGUAGE = 'PTB'
	ACTIVE_STATUS = 'ACTIVE'

	# Create output directory if it doesn't exist
	os.makedirs('output', exist_ok=True)

	# Read the input CSV file
	df = pd.read_csv(INPUT_FILE)
	
	# Filter only active keywords
	active_df = df[df['Status'] == ACTIVE_STATUS].copy()
	
	if active_df.empty:
		print("No active keywords found in input file")
		return
	
	# Prepare data for output
	output_data = []
	seen_keywords = set()  # Track unique keywords
	
	# First pass: add all original keywords and count unique ones
	keywords_to_translate = []
	for _, row in active_df.iterrows():
		keyword = row['Keyword'].strip().lower()  # Normalize keyword
		if keyword not in seen_keywords:
			seen_keywords.add(keyword)
			output_data.append({
				'Action': 'CREATE',
				'Keyword ID': '',
				'Keyword': row['Keyword'],
				'Match Type': MATCH_TYPE,
				'Status': ACTIVE_STATUS,
				'Bid': BID,
				'Campaign ID': CAMPAIGN_ID,
				'Ad Group ID': AD_GROUP_ID
			})
			keywords_to_translate.append(row['Keyword'])
	
	# Second pass: translate unique keywords
	total_to_translate = len(keywords_to_translate)
	print(f"Found {total_to_translate} unique keywords to translate")
	
	for idx, keyword in enumerate(keywords_to_translate, 1):
		translated_kw = translate_text(keyword, TARGET_LANGUAGE)
		if translated_kw:
			print(f"\rTranslating keywords... {idx}/{total_to_translate}", end='', flush=True)
			translated_kw_normalized = translated_kw.strip().lower()
			
			if translated_kw_normalized not in seen_keywords:
				seen_keywords.add(translated_kw_normalized)
				output_data.append({
					'Action': 'CREATE',
					'Keyword ID': '',
					'Keyword': translated_kw,
					'Match Type': MATCH_TYPE,
					'Status': ACTIVE_STATUS,
					'Bid': BID,
					'Campaign ID': CAMPAIGN_ID,
					'Ad Group ID': AD_GROUP_ID
				})
		else:
			print(f"\nWarning: Failed to translate '{keyword}' to {TARGET_LANGUAGE}")

	print()  # New line after progress indicator
	
	# Create DataFrame from processed data
	output_df = pd.DataFrame(output_data)

	# Export to CSV
	output_file = f"output/{CAMPAIGN_ID}_{AD_GROUP_ID}_{TARGET_LANGUAGE}_keyword_import.csv"
	output_df.to_csv(output_file, index=False, na_rep='')

	print(f"Successfully generated ASA import file: {output_file}")
	print(f"Total active keywords found: {len(active_df)}")
	print(f"Unique original keywords: {len(keywords_to_translate)}")
	print(f"Total unique keywords in output (including translations): {len(output_df)}")
	print(f"Duplicate keywords prevented: {(len(active_df) * 2) - len(output_df)}")


if __name__ == "__main__":
	generate_asa_import_file()