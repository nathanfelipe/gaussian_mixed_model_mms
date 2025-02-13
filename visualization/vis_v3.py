import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def plot_gmm_ellipses(ax, gmm, features):
    # For each component, plot an ellipse representing the Gaussian
    for i in range(gmm.n_components):
        mean = gmm.means_[i][:2]  # Use the first two features
        cov = gmm.covariances_[i][:2, :2]
        eigenvals, eigenvecs = np.linalg.eigh(cov)
        # Sort eigenvalues in descending order
        order = eigenvals.argsort()[::-1]
        eigenvals, eigenvecs = eigenvals[order], eigenvecs[:, order]
        angle = np.arctan2(eigenvecs[1, 0], eigenvecs[0, 0]) * 180 / np.pi
        width, height = 2 * np.sqrt(eigenvals)  # 2 standard deviations
        ellipse = Ellipse(mean, width, height, angle=angle, edgecolor='black', facecolor='none', lw=2)
        ax.add_patch(ellipse)

# Load features and model as before
features_df = pd.read_csv('/Users/nathan/CursorProjects/gus_first_project/data/processed/features.csv', index_col=0)
gmm_model = joblib.load('/Users/nathan/CursorProjects/gus_first_project/models/gmm_model.pkl')
features_df['cluster'] = gmm_model.predict(features_df[['ratio_max_width', 'ratio_high_low', 'norm_Bt']])

# Plot using only the first two features for clarity
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(features_df['ratio_max_width'], features_df['ratio_high_low'], c=features_df['cluster'], cmap='viridis', s=50)
ax.set_xlabel('ratio_max_width')
ax.set_ylabel('ratio_high_low')
ax.set_title("GMM Clusters with Gaussian Ellipses")
plot_gmm_ellipses(ax, gmm_model, features_df[['ratio_max_width', 'ratio_high_low']].values)
plt.legend(*scatter.legend_elements(), title="Cluster")
plt.show()