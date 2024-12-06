import pandas as pd
import os


def generate_negative_keyword_file():
	# Define constants
	CAMPAIGN_ID = 1726069162
	AD_GROUP_ID = 1725976928
	MATCH_TYPE = 'EXACT'

	# Read the input CSV file to get keywords
	df = pd.read_csv('output/campaign_1726069162_adgroup_1726011485_keyword_import.csv')

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
	output_file = f"output/{CAMPAIGN_ID}_{AD_GROUP_ID}_negative_keyword_import.csv"
	neg_kw_df.to_csv(output_file, index=False, na_rep='')

	print(f"Successfully generated negative keyword file: {output_file}")
	print(f"Total negative keywords processed: {len(neg_kw_df)}")


if __name__ == "__main__":
	generate_negative_keyword_file()