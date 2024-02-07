import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_word_cloud(combined_df):
    words = [word.lower() for comment in combined_df['commentary'] for word in remove_stopwords(comment)]
    fdist = FreqDist(words)
    common_words = fdist.most_common(100)
    wordcloud = WordCloud(width=800, height=800, background_color='white').generate_from_frequencies(dict(common_words))
    plt.figure(figsize=(12, 9), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

def plot_heatmap(subset_df, x_col, y_col, hue_col):
    plt.figure(figsize=(16, 8))
    pivot_df = pd.pivot_table(subset_df, values=hue_col, index=x_col, columns=y_col, aggfunc=len)
    sns.heatmap(pivot_df, cmap='Blues', annot=True, fmt='g')

def plot_countplots(combined_df, cat_vars):
    for var in cat_vars:
        plt.figure(figsize=(10, 6))
        sns.countplot(x=var, data=combined_df)
        plt.title(var)
        plt.show()

def plot_selected_heatmap(combined_df, selected_batsmen, x_col, y_col, hue_col):
    plt.figure(figsize=(9, 12), dpi=300)
    subset_df = combined_df[combined_df['batsman'].isin(selected_batsmen)][['batsman', x_col, hue_col]]
    pivot_df = pd.pivot_table(subset_df, values=hue_col, index='batsman', columns=x_col, aggfunc=len)
    sns.heatmap(pivot_df, cmap='Blues', annot=True, fmt='g', linewidths=1, linecolor='white', cbar=False, annot_kws={"fontsize": 7})
    plt.xlabel(x_col, fontsize=20)
    plt.ylabel('Batsman', fontsize=20)

def plot_delivery_heatmap(combined_df, selected_batsmen, x_col, y_col, hue_col):
    plt.figure(figsize=(3, 4), dpi=100)
    subset_df = combined_df[combined_df['batsman'].isin(selected_batsmen)][['batsman', x_col, hue_col]]
    pivot_df = pd.pivot_table(subset_df, values=hue_col, index='batsman', columns=x_col, aggfunc=len)
    sns.heatmap(pivot_df, cmap='Blues', annot=True, fmt='g', linewidths=1, linecolor='white', cbar=False, annot_kws={"fontsize": 7})
    plt.xlabel(x_col, fontsize=16)
    plt.ylabel('Batsman', fontsize=16)
    plt.show()

def plot_result_heatmap(combined_df, selected_batsmen, x_col, hue_col):
    plt.figure(figsize=(5, 6), dpi=200)
    subset_df = combined_df[combined_df['batsman'].isin(selected_batsmen)][['batsman', x_col, hue_col]]
    pivot_df = pd.pivot_table(subset_df, values=hue_col, index='batsman', columns=x_col, aggfunc=sum)
    sns.heatmap(pivot_df, cmap='Blues', annot=True, fmt='g', linewidths=1, linecolor='white', cbar=False, annot_kws={"fontsize": 9})
    plt.xlabel(x_col, fontsize=16)
    plt.ylabel('Batsman', fontsize=16)
    plt.show()

def plot_categorical_heatmap(combined_df, selected_batsmen, x_col, y_col, hue_col):
    plt.figure(figsize=(5, 6), dpi=200)
    subset_df = combined_df[combined_df['batsman'].isin(selected_batsmen)][['batsman', x_col, hue_col]]
    pivot_df = pd.pivot_table(subset_df, values=hue_col, index='batsman', columns=x_col, aggfunc=sum)
    sns.heatmap(pivot_df, cmap='Blues', annot=True, fmt='g', linewidths=1, linecolor='white', cbar=False, annot_kws={"fontsize": 9})
    plt.xlabel(x_col, fontsize=16)
    plt.ylabel('Batsman', fontsize=16)
    plt.show()

def main():
    combined_df = pd.read_csv("golddata.csv")
    plot_word_cloud(combined_df)
    subset_df = combined_df[['batsman', 'stageofgame', 'result_n']]
    plot_heatmap(subset_df, 'batsman', 'stageofgame', 'result_n')
    cat_vars = ['result', 'bowler', 'batsman', 'venue', 'pitchtype', 'bowlertype', 'bowlerhand', 'batsmanhand', 'balllength', 'ballline', 'ballspeed', 'ballswing/spin', 'stageofgame']
    plot_countplots(combined_df, cat_vars)
    selected_batsmen = ['Buttler', 'Rahul', 'du Plessis', 'Tilak Varma', 'Hooda', 'Hardik Pandya', 'Shreyas Iyer', 'Shubman Gill', 'Gaikwad', 'Kohli', 'Markram', 'Samson', 'Tripathi']
    plot_selected_heatmap(combined_df, selected_batsmen, 'stageofgame', 'result_n', 'result_n')
    plot_delivery_heatmap(combined_df, selected_batsmen, 'stageofgame', 'result_n', 'result_n')
    plot_result_heatmap(combined_df, selected_batsmen, 'stageofgame', 'result_n')
    plot_categorical_heatmap(combined_df, selected_batsmen, 'pitchtype', 'result_n', 'result_n')

if __name__ == "__main__":
    main()
