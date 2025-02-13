import pandas as pd
import joblib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # This import registers the 3D projection, no direct use.

# Load the features
features_df = pd.read_csv('/Users/nathan/CursorProjects/gus_first_project/data/processed/features.csv', index_col=0)

# Load the trained GMM model
gmm_model = joblib.load('/Users/nathan/CursorProjects/gus_first_project/models/gmm_model.pkl')

# Predict the cluster labels
features_df['cluster'] = gmm_model.predict(features_df[['ratio_max_width', 'ratio_high_low', 'norm_Bt']])

# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(
    features_df['ratio_max_width'], 
    features_df['ratio_high_low'], 
    features_df['norm_Bt'], 
    c=features_df['cluster'], 
    cmap='viridis', 
    s=50
)

ax.set_xlabel('ratio_max_width')
ax.set_ylabel('ratio_high_low')
ax.set_zlabel('norm_Bt')
plt.title("3D Scatter Plot of GMM Clusters")
plt.colorbar(sc, label='Cluster')
plt.show()