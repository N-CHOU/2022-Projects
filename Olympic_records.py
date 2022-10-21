#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set()


# In[2]:


data = pd.read_csv('df_final_features.csv')
data.head()


# In[3]:


data.info


# In[4]:


# color palette
sns.palplot(['#0087AB', '#87CFE0', '#FFFFFF','#FF5C41', '#C43A38'])


# In[5]:


# distribution by gender
# fig, ax = plt.subplots(1, 1, figsize=(20, 10))
# ax.barh(data.index, data['Sex'], color='#87CFE0', label='Male')
m = data.groupby('Sex')['Team'].value_counts()['M']
f = data.groupby('Sex')['Team'].value_counts()['F']
print(m)


# In[6]:


plot1 = pd.concat([m, f], axis=1, join='outer')
plot1
top_countries = data.sort_values(by='GDP_Per_Capita_Constant_LCU_Value')


# In[7]:


# plot1 = plot1.rename(columns={'Team' : 'Male'})
plot1.columns = ['Male', 'Female']


# In[8]:


plot1


# In[9]:


cross_tab_prop = pd.crosstab(index=data['Team'],
                             columns=data['Sex'],
                             normalize="index")
cross_tab_prop


# In[10]:


# finally creating the bar plot
p1 = cross_tab_prop.head(10)
plot = p1.plot(kind='barh', stacked=True, color=['#87CFE0','#FF5C41'], figsize=(10, 6))
plot.grid(False)
plot.set_facecolor('white')
plt.xlabel("Proportion of participants")
plt.ylabel("Top 10 countries")


# In[11]:


data


# In[12]:


# here is what I want, two area charts for summer and winter. Show gender distribution by color
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 1)
gs.update(hspace= -0.78)

axes = list()
colors = ['#0087AB', '#C43A38']

for idx, cls,c in zip(range(2), sorted(data['Season'].unique()), colors):
    axes.append(fig.add_subplot(gs[idx, 0]))
    
    sns.kdeplot(x='Age', data = data[data['Season']==cls], 
               fill=True, ax=axes[idx], cut=0, bw_method=0.25, 
               lw=1.4, hue='Sex', 
               multiple="stack", alpha=0.7)
    
    
    axes[idx].set_ylim(0, 0.04)
    axes[idx].set_xlim(0, 80)
    
    axes[idx].set_yticks([])
    if idx != 2 : axes[idx].set_xticks([])
    axes[idx].set_ylabel('')
    axes[idx].set_xlabel('')
    
    spines = ["top","right","left","bottom"]
    for s in spines:
        axes[idx].spines[s].set_visible(False)
        
    axes[idx].patch.set_alpha(0)
    if idx != 1 : axes[idx].get_legend().remove()
        
plt.show()


# In[13]:


yearwise_groupings = data.groupby('Year')
yearwise_groupings.first()
yearwise_groupings.get_group(1984)


# In[14]:


list(data.columns)


# In[15]:


# number of female participants over the years
athletes_by_gender = data.groupby('Sex')

female_athletes = athletes_by_gender.get_group('F')
female_athletes


# In[16]:


medals = data.groupby('Team')
medals.first()
medals = pd.crosstab(index=data['Team'],
                             columns=data['Medal'],
                             )
medals


# In[17]:


data['Medal'].max()


# In[18]:


top_medals = medals
type(top_medals)
#top_medals.drop("0", axis=1, inplace=True)
top_medals = top_medals.loc[:, [1,2, 3]]
top_medals.head(15)
#medals_by_country = top_medals.plot(kind='bar')


# In[27]:


# lets find the number of athletes every year
# expecting a line plot 
dict(data.dtypes)
# from datetime import datetime


# In[34]:


# converting the datatype of the Year column from  integer to date time
data['Year'] = pd.to_datetime(data['Year'],format='%Y' )


# In[35]:


time_data = data
time_data = time_data.set_index('Year')


# In[37]:


time_data.plot()


# In[ ]:





# In[20]:


#top_medals = top_medals.head(10)
top_medals = top_medals.sort_values('1', ascending=False)
plot = top_medals.plot(kind='bar', color=['#FFFFFF','#FF5C41', '#C43A38'], figsize=(10, 6))
plot.grid(False)
plot.set_facecolor('white')
plt.xlabel("Proportion of participants")
plt.ylabel("Top 10 countries")

