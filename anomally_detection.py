import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
df = pd.read_csv("soil_data.csv", parse_dates=["Timestamp"])

timestamps = df["Timestamp"]
X = df.drop(columns=["Timestamp"])

# normalization: here we do Z-score
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means clustering (k=2)
kmeans = KMeans(n_clusters=2, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# decide which cluster is anomaly:
# assume the smaller cluster = anomalies
# (flip labels if needed)
counts = pd.Series(labels).value_counts()
anomaly_cluster = counts.idxmin()
is_anomaly = (labels == anomaly_cluster).astype(int)

#creats the output file for anomaly_flags.csv
out = pd.DataFrame({
    "Timestamp": timestamps,
    "is_anomaly_point": is_anomaly
})
out.to_csv("anomaly_flags.csv", index=False)
print("Points per cluster:\n", counts.to_dict())

#2D PCA plot for visualization 
pca = PCA(n_components=2)
proj = pca.fit_transform(X_scaled)
plt.figure()
for lab in [0,1]:
    mask = (labels == lab)
    plt.scatter(proj[mask,0], proj[mask,1],
                label=f"{'anomaly' if lab==anomaly_cluster else 'normal'}",
                alpha=0.6, edgecolor='k')
plt.title("PCA of Soil Sensor Data")
plt.xlabel("PC1"); plt.ylabel("PC2")
plt.legend()
plt.tight_layout()
plt.show()

#feature-wise boxplots
plt.figure(figsize=(12,6))
plt.boxplot(X_scaled, labels=X.columns, vert=False)
plt.title("Feature Distributions (Z-score Normalized)")
plt.tight_layout()
plt.show()
