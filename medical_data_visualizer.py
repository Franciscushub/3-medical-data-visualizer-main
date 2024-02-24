import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv',sep=',',header=0)
### id / ['age', 'sex', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']

# Add 'overweight' column
BMI = df['weight'] / ((df['height']/100)**2)
mask = BMI > 25
df['overweight'] = 0
df.loc[mask, ['overweight']] = 1

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    df_cat = pd.melt(df,id_vars =['cardio'],value_vars=value_vars)



    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable','value']).size().reset_index(name='total')

    

    # Draw the catplot with 'sns.catplot()'
    plot = sns.catplot(data=df_cat,col='cardio', x='variable', y='total', kind='bar',hue='value')

    # Get the figure for the output
    fig = plot.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():

    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]


    # Calculate the correlation matrix
    corr = df_heat.corr()


    # Generate a mask for the upper triangle
    mask = np.tril(np.ones_like(corr, dtype=np.bool_), k=-1)
    corr = corr.where(mask)
 
    
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,annot=True,linewidth=.5,fmt=".1f", vmin=-0.2, vmax=0.7,cmap="crest")
    ax.set_title("Correlation Matrix Heatmap")
    

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
