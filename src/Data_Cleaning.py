import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import math
import random
from math import sqrt
import scipy.cluster.hierarchy as sch
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score
import os
import pickle
from flask import Flask, request, jsonify
import requests



def filter_dataframe(combined_df):
    filter_values = [
        '1 run 50-run stand up between the openers. On a length outside off and Shubman Gill pushes this through cover-point for a single ',
        ' 4 runs', ' from round the wicket',
        ' SIX .. 22 off this over. And as smart as hindsight might seem',
        ' wide out Stumped!! He is gone! Stumped down leg. Superb stuff from Jackson. Uthappa overbalanced trying to flick and Chakaravarthy slipped it down leg for the keeper to do the rest. Superb glovework from Sheldon. Made it look so simple despite being slightly blinded by the batter. KKR now have the set man removed. CSK in big trouble. Uthappa st Jackson b Chakaravarthy 28(21) [4s-2 6s-2]',
        # ... (other filter values)
        ' SIX .. crouches'
    ]

    filtered_df = combined_df[combined_df['result'].isin(filter_values)]
    filtered_index = filtered_df.index
    combined_df = combined_df.drop(filtered_index)

    filter_values = [
        ' 5 wides',
        ' 2 wides',
        ' 1 run 50-run stand up between the openers. On a length outside off and Shubman Gill pushes this through cover-point for a single '
    ]

    filtered_df = combined_df[combined_df['result'].isin(filter_values)]
    filtered_index = filtered_df.index
    combined_df = combined_df.drop(filtered_index)

    return combined_df

def map_results(combined_df):
    result_mapping = {' 2 runs': 2, ' no run': 0, 'out': 0, ' 1 run': 1, ' SIX': 6, ' FOUR': 4, ' wide': 1, ' leg byes': 0, ' no ball': 1, ' byes': 0, ' 3 runs': 3}
    combined_df['result_n'] = combined_df['result'].apply(lambda x: result_mapping.get(x, None))
    return combined_df

def merge_dataframes(combined_df, df_bowler, df_batsman):
    combined_df['bowler'] = combined_df['bowler'].apply(str.strip)
    combined_df['batsman'] = combined_df['batsman'].apply(str.strip)

    combined_df = pd.merge(combined_df, df_bowler[['Player Name', 'Bowler Type', 'Hand']], left_on='bowler', right_on='Player Name', how='left')
    combined_df.rename(columns={'Hand': 'bowlerhand'}, inplace=True)
    combined_df.rename(columns={'Bowler Type': 'bowlertype'}, inplace=True)

    combined_df = pd.merge(combined_df, df_batsman[['Player Name', 'Hand']], left_on='batsman', right_on='Player Name', how='left')
    combined_df.rename(columns={'Hand': 'batsmanhand'}, inplace=True)

    combined_df.pop('Player Name_x')
    combined_df.pop('Player Name_y')

    return combined_df

def clean_commentary_column(combined_df):
    combined_df['commentary'] = combined_df['commentary'].astype(str)
    combined_df['commentary'] = combined_df['commentary'].str.replace('[^\w\s]', '')
    return combined_df

def add_length_column(combined_df):
    length_keywords = ['full toss', 'toss', 'slot', 'length ball', 'fuller', 'fullish', 'overpitched', 'short of a length', 'back of a length', 'good length', 'slightly full', 'slightly short', 'yorker', 'volley', 'bouncer', 'shorter', 'short']
    combined_df['length'] = combined_df['commentary'].apply(lambda x: next((w for w in length_keywords if w in x.lower()), None))
    return combined_df

def main():
    df_bowler = pd.read_csv('~/bowlerdetails.csv')
    df_batsman = pd.read_csv('~/batsmandetails.csv')

    combined_df = pd.read_csv("~/bronzedata.csv")
    combined_df = filter_dataframe(combined_df)
    combined_df = map_results(combined_df)
    combined_df = merge_dataframes(combined_df, df_bowler, df_batsman)
    combined_df = clean_commentary_column(combined_df)
    combined_df = add_length_column(combined_df)
    combined_df.to_csv('silverdata.csv', index=False)

if __name__ == "__main__":
    main()
