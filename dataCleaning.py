import pandas as pd
import numpy as np

def clean_data():

    df = pd.read_csv('steam_special_offers.csv')

    df = df.replace(r'^\s*$', np.nan, regex=True)
    df['Reviews'] = df['Reviews'].fillna("No user reviews")
    df['Percent_Discount'] = df['Percent_Discount'].fillna("-0%")
    df['Percent_Discount'] = df['Percent_Discount'].str.replace('-', '')
    df['Release_Date'] = df['Release_Date'].fillna("N/A")
    df['Release_Date'] = df['Release_Date'].str.replace('.', ',')
    df['Title'] = df['Title'].str.replace('.', ',')
    df.to_csv("steam_special_offers.csv")
    


