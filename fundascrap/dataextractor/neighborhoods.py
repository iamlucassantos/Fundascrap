"""
Created on 20/11/2020

@author: Lucas V. dos Santos
"""

import pandas as pd
from datetime import date


# Main action:
# cd fundascrap
# scrapy crawl funda -o houses.csv -t csv
def update_neighbor(filename='houses.csv'):
    """Save houses scraped into a csv file with unique values"""

    # Load most resent scraped data
    df = pd.read_csv(f'../{filename}')
    df['date'] = date.today()

    # Lod history of scraped data
    df_history = pd.read_csv('../data/houses.csv')

    # Convert numeric columns to numbers
    to_num = ['price', 'area1', 'area2', 'rooms']
    df[to_num] = df[to_num].apply(pd.to_numeric, errors='coerce')

    # Update history file with only new houses
    df_new = pd.concat([df, df_history]).drop_duplicates('link')

    # Save updated history file
    df_new.to_csv('../data/houses.csv', index=False, columns=['city', 'buurt', 'title', 'subtitle', 'price', 'rooms', 'area1', 'area2', 'date', 'link'])


def main():
    update_neighbor()


if __name__ == "__main__":
    main()
