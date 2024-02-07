import pandas as pd
import numpy as np

def assign_ball_length(row):
    length = row['length']
    if length in ['volley', 'full toss', 'toss', 'fuller', 'fullish', 'slightly full', 'full']:
        return 'full'
    elif length in ['slot', 'over pitched', 'overpitched']:
        return 'slot'
    elif length == 'yorker':
        return 'yorker'
    elif length in ['length ball', 'back of a length', 'good length', 'short of a length']:
        return 'length'
    elif length in ['slightly short', 'bouncer', 'shorter', 'short']:
        return 'short'
    else:
        return np.nan

def get_delivery_line(commentary):
    away_line = ['outswinger', 'wide', 'outside off', 'outside the off-stump', 'wide outside','outside','away']
    straight_line = ['inline','straight','good length', 'full length', 'yorker', 'full-toss', 'sharp']
    inwards_line = ['inswinger', 'legstump', 'middle off', 'legside',
                    'short-pitched delivery', 'bouncer', 'reverse swing', 'spin','into']

    if any(keyword in commentary.lower() for keyword in away_line):
        return 'away'
    elif any(keyword in commentary.lower() for keyword in straight_line):
        return 'straight'
    elif any(keyword in commentary.lower() for keyword in inwards_line):
        return 'near'
    else:
        return np.NaN

def feature_engineering(combined_df):
    combined_df['balllength'] = combined_df.apply(assign_ball_length, axis=1)
    combined_df['balllength'].interpolate(method='linear', inplace=True)

    options = ['full', 'length', 'short', 'yorker', 'slot']
    mask = combined_df['balllength'].isnull()
    combined_df.loc[mask, 'balllength'] = np.random.choice(options, size=mask.sum())
    combined_df.pop('length')

    combined_df['ballline'] = combined_df['commentary'].apply(get_delivery_line)
    combined_df['ballline'].interpolate(method='linear', inplace=True)
    lines = ['away', 'straight', 'near']
    for i, row in combined_df.iterrows():
        if pd.isna(row['ballline']):
            combined_df.loc[i, 'ballline'] = np.random.choice(lines)

    def get_delivery_speed(commentary, bowlertype):
        if any(keyword in commentary.lower() for keyword in ['quick', 'fast', 'express','pace', 'fast', 'rapid', 'lightning']):
            return 'fast'
        elif any(keyword in commentary.lower() for keyword in ['medium', 'moderate','cutter','back of hand','knuckleball']):
            return 'medium'
        elif any(keyword in commentary.lower() for keyword in ['slow', 'gentle']):
            return 'slow'
        elif bowlertype in ['Spin', 'Slow']:
            return 'slow'
        elif bowlertype in ['Medium', 'Medium-fast']:
            return 'medium'
        else:
            return np.NaN

    combined_df['ballspeed'] = combined_df.apply(lambda x: get_delivery_speed(x['commentary'], x['bowlertype']), axis=1)
    combined_df['ballspeed'] = combined_df['ballspeed'].fillna(combined_df['bowlertype'])

    def get_delivery_swing(commentary):
        if any(keyword in commentary.lower() for keyword in ['away', 'outswinger', 'wide off','wide']):
            return 'away'
        elif any(keyword in commentary.lower() for keyword in ['inswinger', 'googly','off cutter','swing into','inside']):
            return 'into'
        elif any(keyword in commentary.lower() for keyword in ['drift', 'straight','skid','volley']):
            return 'straight'
        else:
            return 'straight'

    combined_df['ballswing/spin'] = combined_df['commentary'].apply(get_delivery_swing)

    def stage_of_game(over):
        if over <= 6:
            return 'powerplay'
        elif over <= 14:
            return 'middleovers'
        else:
            return 'deathovers'

    combined_df['stageofgame'] = combined_df['over'].apply(stage_of_game)

    venue_boundary_sizes = {
        'Wankhede Stadium, Mumbai': 'small',
        'Brabourne Stadium, Mumbai': 'small',
        'Dr DY Patil Sports Academy, Mumbai': 'medium',
        'Maharashtra Cricket Association Stadium, Pune': 'large',
    }

    combined_df['boundary_size'] = combined_df['venue'].map(venue_boundary_sizes)
    combined_df.dropna(inplace=True)

    new_order = ['matchno', 'deliverynumber', 'venue', 'over', 'playerinplay', 'fullcom', 'commentary', 'batting_side', 'batsman', 'batsmanhand', 'bowler', 'pitchtype', 'bowlerhand', 'bowlertype', 'balllength', 'ballline', 'ballspeed', 'ballswing/spin', 'stageofgame', 'boundary_size', 'result', 'result_n']
    reordered_df = combined_df[new_order]

    return reordered_df

def main():
    combined_df = pd.read_csv("silverdata.csv")
    cleaned_and_engineered_df = feature_engineering(combined_df)
    cleaned_and_engineered_df.to_csv("golddata.csv", index=False)

if __name__ == "__main__":
    main()
