"""
max_char_report.py: Builds PDF report to analyze keyword phrases generated in step 1 with max_len > 30.

Project Description: Search Engine Marketing keyword generation for client site built using Elementor.
Author: Bert Rico
Copyright (c) 2024, ByteWise Analytics, LLC
License: All Rights Reserved
Version: 1.0.0
Maintainer: ByteWise Analytics
Email: info@bytewise.app
Status: Development
"""
import sys
import matplotlib.pyplot as plt
import pandas as pd

def generate_report(csv_file_path):
    # Load the generated keywords DataFrame
    kwords_df = pd.read_csv(csv_file_path)

    adgroup_lengths = pd.Series([len(adgrp) for adgrp in kwords_df['Ad Group'].unique()])
    long_adgroups = sum(adgroup_lengths > 30)

    plt.figure(figsize=(9, 6))
    plt.hist(adgroup_lengths, rwidth=0.9, bins=50)
    plt.vlines(x=30, ymin=0, ymax=10, colors='red')
    plt.title(str(long_adgroups) + ' ad group name lengths > 30 (don\'t fit in a headline)',  fontsize=17)
    plt.xlabel('Ad Group Name Lengths', fontsize=15)
    plt.ylabel('Count', fontsize=15)
    plt.yticks(range(11))
    plt.xticks(range(0, 51, 5))
    plt.grid(alpha=0.5)

    # Return the figure to be used in other scripts
    return plt

if __name__ == "__main__":
    # Check if a CSV file path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python max_char_report.py <csv_file_path>")
        sys.exit(1)

    # Get the CSV file path from the command-line argument
    csv_file_path = sys.argv[1]

    # Generate the report using the provided CSV file
    plt_instance = generate_report(csv_file_path)

    # Save the plot as max_char_report.pdf in the /out/ directory (overwrite if exists)
    output_pdf_path = 'out/max_char_report.pdf'
    plt_instance.savefig(output_pdf_path)
    plt.close()

    print('Step 2 complete, moving on to step 3...\n')