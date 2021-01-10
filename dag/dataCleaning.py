import pandas as pd
import numpy as np

def clean_data():

    df = pd.read_csv('/Users/luke/PassionProject/steam_special_offers.csv')

    df = df.replace(r'^\s*$', np.nan, regex=True)
    df['Reviews'] = df['Reviews'].fillna("No user reviews")
    df['Percent_Discount (%)'] = df['Percent_Discount (%)'].fillna("0")
    df['Percent_Discount (%)'] = df['Percent_Discount (%)'].str.replace('-', '')
    df['Percent_Discount (%)'] = df['Percent_Discount (%)'].str.replace('%', '')
    df['Original_Price ($)'] = df['Original_Price ($)'].str.replace('$', '')
    df['Original_Price ($)'] = df['Original_Price ($)'].str.replace('Free to Play', '0')
    df['Discounted_Price ($)'] = df['Discounted_Price ($)'].replace('Free to Play', '0')
    df['Release_Date'] = df['Release_Date'].fillna("N/A")
    df['Release_Date'] = df['Release_Date'].str.replace('.', ',')
    df['Title'] = df['Title'].str.replace('.', ',')
    df.to_csv("steam_special_offers.csv")


    


