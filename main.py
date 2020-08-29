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
reviews_df = reviews_df[(reviews_df['created_at'] > '2019')]
# %%
g = sns.FacetGrid(stats_df, col='subject_type')
g.map(sns.distplot, 'percentage_correct', rug=True, hist=False)
plt.show()
# %%
sns.catplot(x='subject_type', y='percentage_correct', kind='boxen',
            data=stats_df)
plt.show()
# %%
reviews_df['hour'] = reviews_df['created_at'].dt.hour
reviews_df['day'] = reviews_df['created_at'].dt.day
reviews_df['month'] = reviews_df['created_at'].dt.month
reviews_df['year'] = reviews_df['created_at'].dt.year
reviews_df['weekday'] = reviews_df['created_at'].dt.weekday

reviews_df.groupby('hour').count()

# %%

rdf = reviews_df.merge(right=stats_df[['subject_id', 'subject_type']], on='subject_id')
rdf['total_incorrect'] = rdf['incorrect_meaning_answers'] + rdf['incorrect_reading_answers']
sel_hours = rdf['hour'] >= 7
ax = sns.relplot(x='hour', y='total_incorrect', kind='line',
                 hue='subject_type', style='subject_type', data=rdf[sel_hours])
plt.show()

# %%

g = sns.catplot(x='hour', y='total_incorrect',
                col='subject_type',
                data=rdf, kind='boxen')
plt.show()

p = sns.FacetGrid(rdf, col='subject_type')
p.map(sns.distplot, 'hour', rug=True, hist=False)
plt.show()

# %%

temp = rdf.groupby(['weekday', 'month']).mean().reset_index().pivot('weekday', 'month', 'total_incorrect')
sns.heatmap(annot=False, data=temp)
plt.show()
# %%

sns.catplot(x='month', hue='year', col='subject_type', kind='count', data=rdf)
sns.catplot(x='hour', col='subject_type', kind='count', data=rdf)
sns.catplot(x='hour', kind='count', data=rdf)
sns.catplot(x='weekday', kind='count', data=rdf)
plt.show()
# %%

sns.clustermap(data=temp)
# sns.clustermap(data=stats_df[['subject_type','percentage_correct']])
plt.show()
# %%

sns.catplot(x='total_incorrect', kind='count', hue='subject_type', data=rdf)
plt.show()

# %%
# join subjects table on review statistics

subject_df = pd.read_csv('data/subjects.csv')

# don't need date updated from subject table, and hidden is always false so dropping that too
merged_df = stats_df.merge(subject_df.drop('data_updated_at', axis=1), left_on=['subject_id', 'subject_type'],
                           right_on=['id', 'subject_type'],
                           how='inner').drop(['hidden', 'id'], axis=1)

merged_df['subject_type'] = merged_df['subject_type'].astype('category')
merged_df['level'] = merged_df['level'].astype('category')

# %%

# join reviews table on subject_id

rtemp = reviews_df.rename({'created_at': 'review_dt'}, axis=1).drop(['assignment_id', 'spaced_repetition_system_id',
                                                                     'data_updated_at', 'hour', 'day', 'month', 'year',
                                                                     'weekday'], axis=1)
rtemp['total_incorrect'] = rtemp['incorrect_meaning_answers'] + rtemp['incorrect_reading_answers']

rs_df = rtemp.merge(subject_df.drop('data_updated_at', axis=1), left_on='subject_id',
                    right_on='id', how='inner').drop('id', axis=1)


# %%
import statsmodels.api as sm
from patsy import dmatrices

# does type of subject have any predictive power on the percentage?

y, X = dmatrices('percentage_correct ~ subject_type + number_similar + level', data=merged_df, return_type='dataframe')
lm = sm.OLS(y, X)
res = lm.fit()
print(res.summary())



# %%
# time series analysis?

import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
from statsmodels.tsa.api import acf, pacf, graphics

pd.plotting.register_matplotlib_converters()
# Default figure size
sns.mpl.rc('figure',figsize=(16, 6))
# %%
ts = stats_df[['created_at', 'percentage_correct']].set_index('created_at').dropna()
temp = ts.asfreq('1H', method='pad')
# Scale by 100 to get percentages
fig, ax = plt.subplots()
ax = ts.plot(ax=ax)
plt.show()
# %%
mod = AutoReg(ts, 3, old_names=False)
res = mod.fit()
print(res.summary())
# %%
res = mod.fit(cov_type="HC0")
print(res.summary())
# %%
sel = ar_select_order(ts, 13, old_names=False)
sel.ar_lags
res = sel.model.fit()
print(res.summary())
# %%
fig = plt.figure(figsize=(16,9))
fig = res.plot_diagnostics(fig=fig, lags=30)
plt.show()
