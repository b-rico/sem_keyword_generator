"""
main.py: Search Engine Marketing keyword generation for client site built using Elementor.

Author: Bert Rico
Copyright (c) 2024, ByteWise Analytics, LLC
License: All Rights Reserved
Version: 1.0.0
Maintainer: ByteWise Analytics
Email: info@bytewise.app
Status: Development
"""

import subprocess
import pandas as pd

kwords_csv = 'out/keywords.csv'

# Step 1: generate keywords from scraped website
subprocess.run(['python', 'keywords.py'])

# Step 2: Call generate a report to see how many keywords > 30 char
subprocess.run(['python', 'max_char_report.py', kwords_csv])

# Step 3: Process keywords longer than 30 char
subprocess.run(['python', 'split_len.py', kwords_csv])

# Load the original keywords DataFrame from keywords.csv
keywords_df = pd.read_csv('out/keywords.csv')

# Drop the 'Campaign' column
keywords_df = keywords_df.drop(columns=['Campaign'])

# Reorder the remaining columns
ordered_columns = ['Ad Group', 'Criterion Type', 'Keyword', 'Display Links', 'Headline', 'Description']
keywords_df = keywords_df[ordered_columns]

# Save the cleaned-up DataFrame to generated_keywords.csv
output_csv_path = 'out/ad_campaign.csv'
keywords_df.to_csv(output_csv_path, index=False)

print(f'Ad Campaign information saved to {output_csv_path}')