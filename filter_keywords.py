import os


def clean_keyword(keyword):
	"""Clean keyword by removing extra spaces and converting to lowercase"""
	return keyword.strip().lower()


def get_existing_keywords(csv_content):
	"""Extract keywords from CSV content"""
	# Skip header row and get the 'Keyword' column (3rd column)
	lines = csv_content.strip().split('\n')[1:]
	keywords = [line.split(',')[2] for line in lines]
	return set(map(clean_keyword, keywords))


def get_new_keywords(txt_content):
	"""Extract keywords from txt content"""
	# Split by comma and clean each keyword
	keywords = txt_content.replace('\n', '').split(',')
	# Clean keywords and remove duplicates using set
	cleaned_keywords = list(map(clean_keyword, keywords))

	# Check for duplicates and log if found
	duplicate_check = {}
	for keyword in cleaned_keywords:
		if keyword in duplicate_check:
			duplicate_check[keyword] += 1
		else:
			duplicate_check[keyword] = 1

	duplicates = [k for k, v in duplicate_check.items() if v > 1]
	if duplicates:
		print("Warning: Found duplicate keywords in input:")
		for dup in duplicates:
			print(f"- '{dup}' appears {duplicate_check[dup]} times")

	return set(cleaned_keywords)


def read_file(filepath):
	"""Read file content"""
	try:
		with open(filepath, 'r', encoding='utf-8') as file:
			return file.read()
	except Exception as e:
		print(f"Error reading file {filepath}: {str(e)}")
		return None


def write_file(filepath, keywords):
	"""Write unique keywords to file without extra spaces"""
	try:
		# Create directory if it doesn't exist
		os.makedirs(os.path.dirname(filepath), exist_ok=True)

		# Ensure uniqueness one more time and sort
		unique_keywords = sorted(set(keywords))

		# Join keywords with comma, no spaces
		content = ','.join(unique_keywords)

		with open(filepath, 'w', encoding='utf-8') as file:
			file.write(content)
		print(f"Successfully wrote {len(unique_keywords)} unique keywords to {filepath}")
		return True
	except Exception as e:
		print(f"Error writing to file {filepath}: {str(e)}")
		return False


def find_missing_keywords(existing_content, new_content):
	"""Find keywords that exist in new_content but not in existing_content"""
	existing_keywords = get_existing_keywords(existing_content)
	new_keywords = get_new_keywords(new_content)

	# Find keywords that are in new_keywords but not in existing_keywords
	missing_keywords = new_keywords - existing_keywords

	# Log the counts
	print(f"Found {len(existing_keywords)} existing keywords")
	print(f"Found {len(new_keywords)} keywords in new list")
	print(f"Found {len(missing_keywords)} keywords to be added")

	return sorted(missing_keywords)  # Sort alphabetically for consistent output


def main():
	# Define input and output directories and file paths
	input_dir = "input"
	output_dir = "output"
	csv_file = os.path.join(input_dir, "ad_group_keyword_list.csv")
	txt_file = os.path.join(input_dir, "keywords_to_be_added.txt")
	output_file = os.path.join(output_dir, "keywords_to_be_added_clean.txt")

	# Read files
	csv_content = read_file(csv_file)
	txt_content = read_file(txt_file)

	if csv_content is None or txt_content is None:
		return

	# Find missing keywords
	missing_keywords = find_missing_keywords(csv_content, txt_content)

	# Write to output file
	write_file(output_file, missing_keywords)


if __name__ == "__main__":
	main()