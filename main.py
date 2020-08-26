import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='darkgrid')

assignments_df = pd.read_csv('data/assignments.csv')
level_df = pd.read_csv('data/level_progressions.csv')
stats_df = pd.read_csv('data/review_statistics.csv')
reviews_df = pd.read_csv('data/reviews.csv')
# %%
reviews_df['created_at'] = pd.to_datetime(reviews_df['created_at'])
stats_df['created_at'] = pd.to_datetime(stats_df['created_at'])
stats_df = stats_df[(stats_df['created_at'] > '2019')]
# %%
g = sns.FacetGrid(stats_df, col='subject_type')
g.map(sns.distplot, 'percentage_correct', rug=True, hist=False)
plt.show()
# %%
sns.catplot(x='subject_type', y='percentage_correct', kind='boxen',
            data=stats_df)
plt.show()
# %%
stats_df['hour'] = stats_df['created_at'].dt.hour
stats_df['day'] = stats_df['created_at'].dt.day
stats_df['month'] = stats_df['created_at'].dt.month
stats_df['year'] = stats_df['created_at'].dt.year
stats_df['weekday'] = stats_df['created_at'].dt.weekday

stats_df.groupby('hour').count()

# %%

sel_hours = stats_df['hour'] >= 7
ax = sns.relplot(x='hour', y='percentage_correct', kind='line',
                 hue='subject_type', style='subject_type', data=stats_df[sel_hours])
plt.show()
# %%

g = sns.catplot(x='hour', y='percentage_correct',
                col='subject_type',
                data=stats_df, kind='boxen')

p = sns.FacetGrid(stats_df, col='subject_type')
p.map(sns.distplot, 'hour', rug=True, hist=False)
plt.show()

# %%

temp = stats_df.groupby(['weekday', 'month']).mean().reset_index().pivot('weekday', 'month', 'percentage_correct')
sns.heatmap(annot=True, data=temp)
plt.show()
# %%

sns.catplot(x='month', hue='year', col='subject_type', kind='count', data=stats_df)
sns.catplot(x='hour', col='subject_type', kind='count', data=stats_df)
sns.catplot(x='hour', kind='count', data=stats_df)
sns.catplot(x='weekday', kind='count', data=stats_df)
plt.show()
# %%

sns.clustermap(data=temp)
# sns.clustermap(data=stats_df[['subject_type','percentage_correct']])
plt.show()
# %%

# Look at count of errors broken down by reading or meaning type, with/without subject typing
# Also think about streaks

sns.catplot(x='meaning_incorrect', kind='count', data=stats_df)
plt.show()
# %%
