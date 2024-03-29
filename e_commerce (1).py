# -*- coding: utf-8 -*-
"""E-COMMERCE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vu01PCefn1EIO83NYtML8fVbMYk5csOf
"""

import yellowbrick
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import KElbowVisualizer

df = pd.read_excel('/content/drive/MyDrive/cust_data (1).xlsx')

df.head(7)

df.columns

df.shape

df.describe()

df.Gender.value_counts()

plt.figure(figsize = [10,3])
plt.subplot(1,4,1)
sns.countplot(data=df, x='Gender')
plt.show()


plt.subplot(1,2,2)
df['Gender'].value_counts().plot(kind = 'pie',
                                    autopct = '%0.2f%%',
                                    figsize = [10,5],
                                    explode = [0,0.05],
                                    colors = ['#FF1493','#007FFF'])

plt.show()

plt.figure(figsize=(15,5))
plt.subplot(1,2,1)

sns.countplot(data=df, x='Orders',palette='pastel')

# Orders count by each gender:

plt.subplot(1,2,2)
sns.countplot(data=df, x='Orders',hue='Gender',palette='dark')

plt.suptitle("Overall Orders VS Gender wise Orders")
plt.show()

df.head()

colum=list(df.columns[3:])
colum

def feat_list(lst):

    plt.figure(figsize=(30,30))

    for i,col in enumerate(lst,1):

        plt.subplot(6,6,i)
        sns.boxplot(data=df,x=df[col])

#
feat_list(colum)

plt.figure(figsize=(25,15))

dff = df.iloc[:,3: ].corr()
sns.heatmap(dff, annot = True, fmt = '0.2f',cmap='plasma')

plt.show()

df.iloc[:,2:].hist(figsize=(50,50),color='red')
plt.show()

df['Orders'].hist(figsize=(5,3),color='green')
plt.show()

new_df = df.copy()
new_df.iloc[:,2:].sum(axis=0)

new_df['Total_Search'] = new_df.iloc[:,2:].sum(axis=1)
new_df['Total_Search'].head(11)

new_df.head()

new_df.sort_values('Total_Search',ascending=False).head()

plt.figure(figsize=(10,5))

plt_data = new_df.sort_values('Total_Search',ascending=False)[['Cust_ID','Gender','Total_Search']].head(10)

sns.barplot(data=plt_data,
            x='Cust_ID',
            y='Total_Search',
            hue='Gender',
            order=plt_data.sort_values('Total_Search',ascending = False).Cust_ID)

plt.title("Top 10 Cust_ID based on Total Searches")

plt.show()

plt.figure(figsize=(10,5))

plt_data = new_df.sort_values('Total_Search',ascending=False)[['Cust_ID','Gender','Total_Search']].head(1000)

sns.scatterplot(plt_data, x = 'Total_Search', y = 'Cust_ID',hue = 'Gender')

x = df.iloc[:,2: ].values
x

x.shape

scale = MinMaxScaler()
features = scale.fit_transform(x)
features

inertia = []
for i in range(1,16):
    k_means = KMeans(n_clusters=i)

    k_means = k_means.fit(features)

    inertia.append(k_means.inertia_)

print(len(inertia))

plt.figure(figsize=(20,7))

plt.subplot(1,2,1)
plt.plot(range(1,16), inertia, 'bo-')

plt.xlabel('No of clusters'), plt.ylabel('Inertia')


plt.subplot(1,2,2)

kmeans = KMeans()

visualize = KElbowVisualizer(kmeans,k=(1,16))
visualize.fit(features)

plt.suptitle("Elbow Graph and Elbow Visualizer")
visualize.poof()

plt.show()

model = KMeans(n_clusters=3)
model = model.fit(features)

X = model.predict(features)
y_km = model.predict(features)
centers = model.cluster_centers_

centers

print(X)

df['Cluster'] = pd.DataFrame(X)
df.to_csv("Cluster_data", index=False)
df['Cluster'].head()

df.tail()

df['Cluster'].value_counts()

plt.figure(figsize=(5,5))
sns.countplot(data=df,x='Cluster')

plt.show

c_df = pd.read_csv('Cluster_data')
c_df.head()

c_df['Total Search'] = c_df.iloc[:,3:38].sum(axis=1)
c_df['Total Search'].head()

#CLUSTER ANALYSI-0
clu_0 = c_df.groupby(['Cluster','Gender'],as_index=False).sum().query('Cluster == 0')
clu_0

plt.figure(figsize=(15,6))
plt.subplot(1,3,1)
sns.countplot(data=c_df.query('Cluster == 0'),x='Gender')
plt.title('Customers count')
#
plt.subplot(1,3,2)
sns.barplot(data=clu_0,x='Gender',y='Total Search')
plt.title('Total Searches by Gender')
plt.suptitle('No. of Customers and their Total Searches in "Cluster 0"')
#
plt.subplot(1,3,3)
sns.barplot(data=clu_0,x='Orders',y='Total Search',hue='Gender')
plt.title('Order Count')
plt.show()

#CLUSTER ANALYSIS-1
clu_1 = c_df.groupby(['Cluster','Gender'],as_index=False).sum().query('Cluster == 1')
clu_1

plt.figure(figsize=(15,6))
plt.subplot(1,3,1)
sns.countplot(data=c_df.query('Cluster == 1'),x='Gender')
plt.title('Customers count')
#
plt.subplot(1,3,2)
sns.barplot(data=clu_1,x='Gender',y='Total Search')
plt.title('Total Searches by Gender')
plt.suptitle('No. of Customers and their Total Searches in "Cluster 1"')
#
plt.subplot(1,3,3)
sns.barplot(data=clu_1,x='Orders',y='Total Search',hue='Gender')
plt.title('Order Count')
plt.show()

#CLUSTER ANALYSIS-2
clu_2 = c_df.groupby(['Cluster','Gender'],as_index=False).sum().query('Cluster == 2')
clu_2

plt.figure(figsize=(15,6))
plt.subplot(1,3,1)
sns.countplot(data=c_df.query('Cluster == 2'),x='Gender')
plt.title('Customers count')
#
plt.subplot(1,3,2)
sns.barplot(data=clu_2,x='Gender',y='Total Search')
plt.title('Total Searches by Gender')
plt.suptitle('No. of Customers and their Total Searches in "Cluster 2"')
#
plt.subplot(1,3,3)
sns.barplot(data=clu_2,x='Orders',y='Total Search',hue='Gender')
plt.title('Order Count')
plt.show()

#OVERALL ANALYSIS
final_df = c_df.groupby(['Cluster'],as_index=False).sum()
final_df

plt.figure(figsize=(10,5))
sns.countplot(data=c_df,x='Cluster',hue='Gender')
plt.title('Total Customers on each Cluster')
#
plt.show()

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
sns.barplot(data=final_df,x='Cluster',y='Total Search')

plt.title('Total Searches by each group')
#
plt.subplot(1,2,2)
sns.barplot(data=final_df,x='Cluster',y='Orders')

plt.title('Prior Orders by each group')
plt.suptitle('No. of times customers searched the products and their prior Orders')
#
plt.show()

"""#CONCLUSION
Among 30,000 customers Cluster 1 has 12432 customers with very few prior orders, although have most searches performed. There are 9128 customers in Cluster 0 with very frequent searches and average prior orders. And cluster 2 has average prior orders and average searches with 8440 customers.

Cluster 1 has the most customers but their prior orders is only 7560.Based on the prior orders cluster 0 is at the top with 10x more prior orders than cluster 1.Cluster 2 has the least customers but has 37649 prior orders thats almost 500% greater than cluster 1.

Cluster 1 has most number of searches with the count of 81477.Cluster 0 has 64573 searches.Cluster 2 has the least number ofsearches with the count of 60093.
"""