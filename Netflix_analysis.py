#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()


# In[2]:


import datetime as datetime


# In[3]:


data = pd.read_csv('NetflixOriginals.csv')
data


# In[4]:


# cleaning and pre processing
# creating the string ->float year column
data['Year'] = data['Premiere'].str[-4:]
# now converting it to float
data = data.astype({'Year':'float64'})
data


# In[5]:


# now we convert the data type of the Premiere column into date time
data["Premiere"] =  pd.to_datetime(data["Premiere"])
data


# In[6]:


data.info()


# In[7]:


data['Genre'].unique()


# In[8]:


# Color palette
sns.palplot(['#730f2a', '#ff5482', '#bf2c53', '#037312', '#2cbf3f'])
palette = ['#730f2a', '#ff5482', '#bf2c53', '#037312', '#2cbf3f']


# In[9]:


from wordcloud import WordCloud


# In[10]:


#text = data['Genre']
text = " ".join(cat for cat in data.Genre)
word_cloud = WordCloud(collocations = False, background_color = 'white', width = 6000, height = 4000, colormap='PiYG').generate(text)


# In[11]:


plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
# plt.figure(figsize=(15, 8))
plt.show()


# In[12]:


# sorting the data according to IMDB score and then looking at the top entries

score_sorted = data.sort_values(by='IMDB Score', ascending=False)
score_sorted


# In[13]:


# changing the column name gor IMDB score


# In[14]:


# changing the index of the dataframe
rdata = data


# In[ ]:





# In[15]:


score_sorted.head(10).plot(x='Title', y='IMDB Score', figsize=(10, 10), kind='bar', color='#037312')
plt.xticks(rotation=45)
plt.grid(False)
ax = plt.gca()
ax.set_facecolor('white')


# In[16]:


# now we want to drill down on the korean movies followed by the most popular languages
# lets look at the genres available
# explode based on genre
gdata = data


# In[17]:


gdata = gdata.rename(columns={'IMDB Score':'IMDB'})


# In[18]:


gdata = pd.DataFrame(gdata.Genre.str.split('/').tolist(), index=gdata.IMDB).stack()
gdata


# In[19]:


gdata = gdata.reset_index([0, 'IMDB'])
gdata


# In[20]:


gdata = gdata.rename(columns={0:'Genre'})


# In[21]:


# doing the same for language
data['Language'].unique()


# In[22]:


data = data.rename(columns={'IMDB Score':'IMDB'})


# In[23]:


ldata = data
ldata = pd.DataFrame(ldata.Language.str.split('/').tolist(), index=ldata.IMDB).stack()
ldata


# In[24]:


ldata = ldata.reset_index([0, 'IMDB'])
ldata


# In[25]:


ldata = ldata.rename(columns={0:'Language'})


# In[26]:


ldata['Language'].unique()


# In[27]:


# visualizing frequency of appearance 
fig, ax = plt.subplots()
ldata['Language'].value_counts().head(10).plot(ax=ax, kind='bar', color='#bf2c53', figsize=(10, 10))
plt.grid(False)
ax.set_facecolor('white')


# In[28]:


language_groups = ldata.groupby('Language')
language_groups


# In[29]:


# selecting shows that are in korean
kr = ['Korean', 'English/Korean']
korean = data[data['Language'].isin(kr)]


# In[30]:


korean


# In[31]:


# plotting time series data

korean.plot(x='Title', y='IMDB', figsize=(10, 10), kind='bar')
plt.grid(False)
ax.set_facecolor('white')


# In[125]:


data2 = pd.read_csv('Kdrama_2.csv')
data2


# In[126]:


data2.info()


# In[127]:


# cleaning watch time
data2['Watch Time'] = data2['Watch Time'].str[:-3]
data2


# In[128]:


# converting it to float
# before that, we need to deal with the missing values. Here, we can replace them with the mean of the rest

# calculating this mean

# selecting the non nulls
watched = data2
watched = watched.replace(to_replace="__", value="NaN")
watched = watched.replace(to_replace="____", value="NaN")
watched
rated = watched
data2 = watched


# In[129]:


# Now we have a dataset with no missing values, everything has been replaced but null.
# dropping this null to obtain the means
watched.drop(watched[watched['Watch Time'] == 'NaN'].index, inplace = True)


# In[130]:


# Now we calculate the mean 
# converting to float
watched = watched.astype({'Watch Time':'float64'})
mean_watchtime = watched['Watch Time'].mean()
mean_watchtime


# In[99]:


# doing the same for Drama rating
rated.drop(rated[rated['Drama Rating'] == 'NaN'].index, inplace=True)


# In[100]:


rated = rated.astype({'Drama Rating':'float64'})
mean_rating = rated['Drama Rating'].mean()
mean_rating


# In[131]:


# Now we make the replacements in data2
data2['Watch Time'] = data2['Watch Time'].replace(to_replace="NaN", value=mean_watchtime)
data2['Drama Rating'] = data2['Drama Rating'].replace(to_replace="NaN", value=mean_rating)
data2


# In[132]:


data2 = data2.astype({'Watch Time':'float64'})
data2 = data2.astype({'Drama Rating':'float64'})
data2


# In[133]:


data2.info()


# In[134]:


# Handling the year of release column
data2['Year of Release'].unique()


# In[135]:


# my plan here is to get rid of the brackets and then keep only the first 4 characters


# step 1: getting rid of the round brackets 
data2['Year of Release'] = data2['Year of Release'].str[1:-1]


# In[136]:


# we only care about the first year when it started so we consider the first 4 characters in all of them
data2['Year'] = data2['Year of Release'].str[:4]
data2.head()


# In[137]:


data2.info()


# In[117]:


data2['Year'].unique()


# In[118]:


data2['Year'].str[4:]


# In[109]:


data3 = data2


# In[113]:


# step 2.5: dropping rows that have (,) as values in them so that conversion is possible
data3.drop(data3[data3['Year'] == 'I) ('].index, inplace = True)
data3['Year'].unique()


# In[82]:


str(data3['Year']).strip()


# In[111]:


data3['Year'] = str(data3['Year'])


# In[119]:


# step 3: converting the type of the year column to datetime
# data2['Year of Release'] = data2['Year of Release'].str()
# data3['Year'] = pd.to_datetime(data3['Year'])
# data3 = data3.astype({'Year':'float64'})


# In[90]:


data3['Year'].unique()


# In[138]:


#### Okay so the year situation is not working out rn, I'll have to come back to this later
data2


# In[139]:


# lets remove the \n from the Genre now
data2['Genre'] = data2['Genre'].str[1:]
data2['Year of Release'] = data2['Year of Release'].str[:4]
data2


# In[140]:


data2 = data2.drop(['Year'], axis=1)
data2


# In[185]:


# lets try to plot the year of release column without converting it to date time
fig, ax = plt.subplots()
data2['Year of Release'].value_counts().head(10).plot(ax=ax, kind='bar', color='#ff5482', figsize=(10, 10))
plt.grid(False)
fig.text(0.97, 1, 'Distribution of shows throughout the years', fontweight='bold', fontfamily='serif', fontsize=15, ha='right')  
ax.set_facecolor('white')


# In[143]:


data3 = data2


# In[147]:


data3['Year of Release'].unique()


# In[146]:


data3.drop(data3[data3['Year of Release'] ==  'I) ('].index, inplace = True)
data3


# In[149]:


# data2['Drama Rating'] = data2['Drama Rating'].replace(to_replace="NaN", value=mean_rating)
data3['Year of Release'] = pd.to_datetime(data3['Year of Release'], format='%y')
data3


# In[152]:


data2.info()


# In[155]:


data3['Year of Release'] = pd.DatetimeIndex(data3['Year of Release']).year


# In[158]:


data2 = data3


# In[160]:


data2


# In[164]:


# lets try to plot the year of release column without converting it to date time


# In[162]:


df_sorted = data2.sort_values('Year of Release')


# In[163]:


df_sorted


# In[186]:


fig, ax = plt.subplots()
df_sorted['Year of Release'].value_counts().plot(ax=ax, kind='bar', color='#bf2c53', figsize=(10, 10))
plt.grid(False)
fig.text(0.97, 1, 'Distribution of shows throughout the years', fontweight='bold', fontfamily='serif', fontsize=15, ha='right')  
ax.set_facecolor('white')


# In[188]:


# lets try a line chart
fig, ax = plt.subplots(1, 1, figsize=(8, 8))

ax.scatter(x='Year of Release', y='Drama Rating',data=df_sorted, color='#037312')
plt.grid(False)
fig.text(0.97, 1, 'Ratings recieved by shows throughout the years', fontweight='bold', fontfamily='serif', fontsize=15, ha='right')  
ax.set_facecolor('white')


# In[182]:


# so I have this dumbass outlier that I need to somehow get rid of but I have no clue how. 
palette
sns.palplot(palette)


# In[183]:


palette


# In[ ]:


# The next target is to use an NLP model to better understand the genres and the synopsis in the previous notebook


# In[193]:


shortened_palette = ['#bf2c53', '#037312']
text = " ".join(cat for cat in data2.Genre)
word_cloud = WordCloud(collocations = False, background_color = 'white', width = 6000, height = 4000, colormap='PiYG').generate(text)

plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
# plt.figure(figsize=(15, 8))
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




