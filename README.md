# AnomalyDetection
Python project that uses K-Means clustering on 8-dimensional soil sensor data to flag point anomalies (weird sensor readings) and visualize them with PCA and boxplots.
How It Works

Load & parse the CSV (pandas).

Z-score normalize all 8 features so they share the same scale.

Run K-Means (k=2) in the 8-D space to split data into two clusters.

Label the smaller cluster as anomalies (is_anomaly_point = 1).

Save results to anomaly_flags.csv.

Visualize with PCA (8D → 2D) and feature boxplots.


<img width="624" alt="Screen Shot 2025-06-09 at 9 59 02 AM" src="https://github.com/user-attachments/assets/b9dab512-5dcd-4be2-8b7a-7ce9b3d11feb" />

<img width="635" alt="Screen Shot 2025-06-09 at 9 59 16 AM" src="https://github.com/user-attachments/assets/645576cc-c66b-43e1-8784-931f2361d8c2" />
