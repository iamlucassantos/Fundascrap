"""
Created on 20/11/2020

@author: Lucas V. dos Santos
"""

import pandas as pd
import numpy as np



def json_reader(filename, to_num):
    df = pd.read_json(f'../{filename}')






def main():
    json_reader('posts.json')


if __name__ == "__main__":
    main()
