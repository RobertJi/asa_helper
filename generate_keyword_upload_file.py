import pandas as pd
import os


def generate_asa_import_file():
	# Define constants
	CAMPAIGN_ID = 1715185383
	AD_GROUP_ID = 1716434258
	MATCH_TYPE = 'BROAD'
	BID = 1.5

	# Create output directory if it doesn't exist
	os.makedirs('output', exist_ok=True)

	# Read the input CSV file
	df = pd.read_csv('input/ad_group_keyword_list.csv')

	# Create the data with explicit values for each row
	data = {
		'Action': ['CREATE'] * len(df),
		'Keyword ID': [''] * len(df),
		'Keyword': df['Keyword'].tolist(),
		'Match Type': [MATCH_TYPE] * len(df),
		'Status': df['Status'].tolist(),
		'Bid': [BID] * len(df),
		'Campaign ID': [CAMPAIGN_ID] * len(df),
		'Ad Group ID': [AD_GROUP_ID] * len(df)
	}

	# Create DataFrame from the explicit data dictionary
	asa_df = pd.DataFrame(data)

	# Export to CSV with explicit empty_value parameter
	output_file = 'output/keyword_import.csv'
	asa_df.to_csv(output_file, index=False, na_rep='')

	print(f"Successfully generated ASA import file: {output_file}")
	print(f"Total keywords processed: {len(asa_df)}")


if __name__ == "__main__":
	generate_asa_import_file()