import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# Load the features (assuming you've saved them as features.csv)
features_df = pd.read_csv('/Users/nathan/CursorProjects/gus_first_project/data/processed/features.csv', index_col=0)

# Load the trained GMM model from your /models directory
gmm_model = joblib.load('/Users/nathan/CursorProjects/gus_first_project/models/gmm_model.pkl')  # adjust path/extension if needed

# Predict cluster labels for each data point
features_df['cluster'] = gmm_model.predict(features_df[['ratio_max_width', 'ratio_high_low', 'norm_Bt']])

# Create pairwise scatter plots colored by cluster
sns.pairplot(features_df, vars=['ratio_max_width', 'ratio_high_low', 'norm_Bt'], hue='cluster', palette='viridis')
plt.suptitle("Pairwise Scatter Plots of Clusters", y=1.02)
plt.show()