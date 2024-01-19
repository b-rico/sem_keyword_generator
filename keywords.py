"""
keywords.py: Generates keyword phrases by scraping a website.

Project Description: Search Engine Marketing keyword generation for client site built using Elementor.
Author: Bert Rico
Copyright (c) 2024, ByteWise Analytics, LLC
License: All Rights Reserved
Version: 1.0.0
Maintainer: ByteWise Analytics
Email: info@bytewise.app
Status: Development
"""
if __name__ == "__main__":
    # import required libraries/packages 
    import os
    from dotenv import load_dotenv
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    # load environment for variables in the .env file in the .gitignore
    load_dotenv()

    # set variables
    client_page = os.environ.get('client_page_url')
    client_svc_name_sel = '.elementor-cta__title' 
    client_svc_desc_sel = '.elementor-cta__description'
    client_svc_link_sel = '.elementor-cta__button'
    campaign_name = [os.environ.get('campaign_name')]
    keywords = 'data/keywords.txt'
    with open(keywords, 'r') as file:
        keywords_from_file = file.read().strip()
    keywords = keywords_from_file.split('|')

    # environment variable error handling
    if client_page is None:
            raise ValueError('"client_page_url" environment variable not set')
    if campaign_name is None:
            raise ValueError('"campaign_name" environment variable not set')
    if not keywords_from_file:
        raise ValueError('No keywords found in the file.')

    # parse html content
    resp = requests.get(client_page)
    soup = BeautifulSoup(resp.text, 'lxml')

    svc_name = [name.text.strip() for name in soup.select(client_svc_name_sel)]
    svc_desc = [name.text.strip() for name in soup.select(client_svc_desc_sel)]
    svc_urls = [url['href'] for url in soup.select(client_svc_link_sel)]


    # create dataframe with variables
    svc_df = pd.DataFrame({'name': svc_name, 'desc': svc_desc, 'url': svc_urls})

    # function to generate keywords
    def generate_keywords(topics, keywords, desc_list, url_list, match_types=['Exact', 'Phrase', 'Broad'],
                           campaign=campaign_name):
        
        col_names = ['Campaign', 'Ad Group', 'Keyword', 'Criterion Type', 'Description', 'Display Links']
        campaign_keywords = []

        for topic, desc, urls in zip(topics, desc_list, url_list):
            for word in keywords:
                for match in match_types:
                    if match == 'Broad':
                        keyword = '+' + ' +'.join([topic.lower().replace(' ', ' +'), 'in', word.replace(' ', ' +')])
                    else:
                        keyword = topic.lower() + ' in ' + word
                    row = [campaign, topic, keyword, match, desc, urls]
                    campaign_keywords.append(row)
                
        for topic, desc, urls in zip(topics, desc_list, url_list):
            for word in keywords:
                for match in match_types:
                    if match == 'Broad':
                        keyword = '+' + ' +'.join([word.replace(' ', ' +'), topic.lower().replace(' ', ' +')])
                    else:
                        keyword = word + ' ' + topic.lower()
                    row = [campaign, topic, keyword, match, desc, urls]
                    campaign_keywords.append(row)

        return pd.DataFrame.from_records(campaign_keywords, columns=col_names)
    topics = svc_df['name']
    kwords_df = generate_keywords(topics,keywords,svc_desc,svc_urls)

    # Save the DataFrame to a CSV file in the /out/ directory (overwrite if exists)
    output_csv_path = 'out/keywords.csv'  # Adjust the file name if needed
    kwords_df.to_csv(output_csv_path, index=False, mode='w')

    print('\nStep 1 complete, moving on to step 2...\n')