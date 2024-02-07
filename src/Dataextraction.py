import pandas as pd
import os

def clean_c(df1, fb, sb, matno, venue, pitchtype):
    df2 = df1.iloc[:, 3:].copy()
    df2['batting_side'] = sb
    df2 = df2.dropna(subset=['Number1'])
    df2[['playerinplay', 'result', 'commentary']] = df2['Like2'].str.split(',', n=2, expand=True)

    for index, row in df2.iterrows():
        if isinstance(row['Lik1'], str) and row['Lik1'].strip().lower() == 'out':
            if row['result'] is not None and row['commentary'] is not None:
                new_commentary = row['result'] + " " + row['commentary']
            elif row['result'] is not None:
                new_commentary = row['result']
            else:
                new_commentary = row['commentary']
            df2.loc[index, 'commentary'] = new_commentary
            df2.loc[index, 'result'] = row['Lik1']

    df2.pop('Lik1')

    df3 = df1.iloc[:, :3].copy()
    df3['batting_side'] = fb
    df3 = df3.dropna(subset=['Number'])
    df3[['playerinplay', 'result', 'commentary']] = df3['Like'].str.split(',', n=2, expand=True)

    for index, row in df3.iterrows():
        if isinstance(row['Like1'], str) and row['Like1'].strip().lower() == 'out':
            if row['result'] is not None and row['commentary'] is not None:
                new_commentary = row['result'] + " " + row['commentary']
            elif row['result'] is not None:
                new_commentary = row['result']
            else:
                new_commentary = row['commentary']
            df3.loc[index, 'commentary'] = new_commentary
            df3.loc[index, 'result'] = row['Like1']

    df3.pop('Like1')

    df2 = df2.sort_values('Number1')
    df3 = df3.sort_values('Number')
    df2 = df2.rename(columns={'Number1': 'over', 'Like2': 'fullcom'})
    df3 = df3.rename(columns={'Number': 'over', 'Like': 'fullcom'})
    merged_df = pd.concat([df3, df2], ignore_index=True)

    merged_df[['bowler', 'batsman']] = merged_df['playerinplay'].str.split(" to ", expand=True)
    merged_df['matchno'] = matno
    merged_df['venue'] = venue
    merged_df['pitchtype'] = pitchtype

    return merged_df


def main():
    df_bowler = pd.read_csv('~/bowlerdetails.csv')
    df_batsman = pd.read_csv('~/batsmandetails.csv')

    df_match = pd.read_csv('~/IPL_Matches_2022.csv')
    df_match = df_match.iloc[4:]
    df_match['MatchNumber'] = df_match['MatchNumber'].astype(int)
    df_match = df_match.sort_values('MatchNumber')
    df_match = df_match[['MatchNumber', 'Team1', 'Team2', 'Venue']]
    df_match['MatchNumber'] = df_match['MatchNumber'] + 202200
    df_match = df_match.reset_index(drop=True)

    folder_path = '~/ipl/'
    files = os.listdir(folder_path)
    csv_files = [f for f in files if f.endswith('.csv')]  # filter only csv files

    dfs = []

    i = 0
    for file in csv_files:
        df = pd.read_csv(folder_path + file)
        cleaned_df = clean_c(df, df_match['Team1'][i], df_match['Team2'][i], df_match['MatchNumber'][i],
                             df_match['Venue'][i], df_pitch['pitchtype'][i])
        dfs.append(cleaned_df)
        i = i + 1

    # concatenate all dataframes into a single one
    combined_df = pd.concat(dfs, ignore_index=True)

    combined_df['deliverynumber'] = range(1, len(combined_df) + 1)
    combined_df['deliverynumber'] = [f"{i:05}" for i in range(1, len(combined_df) + 1)]
    combined_df.to_csv('~/bronzedata.csv', index=False)


if __name__ == "__main__":
    main()
