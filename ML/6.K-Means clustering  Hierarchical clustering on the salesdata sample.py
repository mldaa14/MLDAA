import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("sales_data_sample.csv", encoding="latin1")

print(df.head())
print(df.tail())
print(df.shape)
print(df.shape[0])
print(df.columns)
print(df.dtypes)
df.info()
print(df.describe())

print(df.isnull().sum())
print(df.isnull().sum().sum())
print(df.isnull().mean() * 100)

df = df.dropna()
df = df.fillna(df.select_dtypes(include=np.number).mean())

print(df.duplicated().sum())
df = df.drop_duplicates()

print(df.select_dtypes(include='object').columns)
print(df.select_dtypes(include=np.number).columns)
print(df.select_dtypes(include='object').shape[1])
print(df.select_dtypes(include=np.number).shape[1])

X = df[['QUANTITYORDERED', 'PRICEEACH', 'SALES']]

print(X.head())
print(X.shape)
print(X.describe())

X.hist(figsize=(10, 5))
plt.show()

X.boxplot(figsize=(10, 5))
plt.show()

print(X.corr())

sns.heatmap(X.corr(), annot=True)
plt.show()

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(X_scaled[:5])

from sklearn.cluster import KMeans

inertia = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

print(inertia)

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertia, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

print(clusters)

df['Cluster'] = clusters

print(df.head())
print(df['Cluster'].value_counts())
print(kmeans.cluster_centers_)

centers = scaler.inverse_transform(kmeans.cluster_centers_)
print(centers)

print("Inertia:", kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters)
plt.xlabel('Quantity Ordered')
plt.ylabel('Price Each')
plt.title('K-Means Clustering')
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(df['QUANTITYORDERED'], df['SALES'], c=df['Cluster'])
plt.xlabel('Quantity Ordered')
plt.ylabel('Sales')
plt.title('Sales Data K-Means Clustering')
plt.show()

print(df.groupby('Cluster')[['QUANTITYORDERED', 'PRICEEACH', 'SALES']].mean())
print(df.groupby('Cluster').size())

from scipy.cluster.hierarchy import dendrogram, linkage

linked = linkage(X_scaled, method='ward')

plt.figure(figsize=(10, 6))
dendrogram(linked)
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Data Points')
plt.ylabel('Distance')
plt.show()

from sklearn.cluster import AgglomerativeClustering

hc = AgglomerativeClustering(
    n_clusters=3,
    linkage='ward'
)

hc_clusters = hc.fit_predict(X_scaled)

print(hc_clusters)

df['Hierarchical_Cluster'] = hc_clusters

print(df.head())
print(df['Hierarchical_Cluster'].value_counts())

plt.figure(figsize=(8, 5))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=hc_clusters)
plt.xlabel('Quantity Ordered')
plt.ylabel('Price Each')
plt.title('Hierarchical Clustering')
plt.show()

print("K-Means Clusters:")
print(df['Cluster'].value_counts())

print("\nHierarchical Clusters:")
print(df['Hierarchical_Cluster'].value_counts())

df.to_csv("sales_clustered.csv", index=False)