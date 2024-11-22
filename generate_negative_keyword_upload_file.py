import pandas as pd
import os


def generate_negative_keyword_file():
	# Define constants
	CAMPAIGN_ID = 1715185383
	AD_GROUP_ID = 1716434258
	MATCH_TYPE = 'EXACT'

	# Read the input CSV file to get keywords
	df = pd.read_csv('input/ad_group_keyword_list.csv')

	# Get keywords from the input file
	negative_keywords = df['Keyword'].tolist()

	# Create output directory if it doesn't exist
	os.makedirs('output', exist_ok=True)

	# Create data dictionary
	data = {
		'Action': ['CREATE'] * len(negative_keywords),
		'Keyword ID': [''] * len(negative_keywords),
		'Negative Keyword': negative_keywords,
		'Match Type': [MATCH_TYPE] * len(negative_keywords),
		'Campaign ID': [CAMPAIGN_ID] * len(negative_keywords),
		'Ad Group ID': [AD_GROUP_ID] * len(negative_keywords)  # Empty for campaign level negative keywords
	}

	# Create DataFrame
	neg_kw_df = pd.DataFrame(data)

	# Export to CSV
	output_file = 'output/negative_keyword_import.csv'
	neg_kw_df.to_csv(output_file, index=False, na_rep='')

	print(f"Successfully generated negative keyword file: {output_file}")
	print(f"Total negative keywords processed: {len(neg_kw_df)}")


if __name__ == "__main__":
	generate_negative_keyword_file()