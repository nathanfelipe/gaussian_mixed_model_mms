#!/usr/bin/env python3
"""
clustering.py

This script trains a Gaussian Mixture Model (GMM) on the engineered features and saves the model.
"""

import os
import pandas as pd
from sklearn.mixture import GaussianMixture
import joblib

def train_gmm(features_df, n_components=4, covariance_type='full', random_state=42):
    """
    Trains a GMM with the specified number of components and covariance type.
    
    Parameters:
        features_df (pd.DataFrame): DataFrame containing the features for clustering.
        n_components (int): Number of clusters (default is 4).
        covariance_type (str): Type of covariance to use (default 'full').
        random_state (int): Random seed for reproducibility.
    
    Returns:
        gmm (GaussianMixture): Trained GMM model.
    """
    gmm = GaussianMixture(
        n_components=n_components,
        covariance_type=covariance_type,
        random_state=random_state
    )
    gmm.fit(features_df)
    return gmm

def save_model(model, model_path):
    """
    Saves the trained model to disk using joblib.
    
    Parameters:
        model: The model object to be saved.
        model_path (str): File path where the model will be saved.
    """
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

def main():
    # Load engineered features from a CSV or DataFrame.
    # For testing purposes, let's assume you've saved your features from feature_engineering.py.
    # Alternatively, you can import process_all_spectra from feature_engineering and process your dummy data.
    features_csv = "/Users/nathan/CursorProjects/gus_first_project /data/processed/features.csv"  # Update this if needed.
    
    if not os.path.exists(features_csv):
        raise FileNotFoundError(f"{features_csv} not found. Ensure you have generated your features first.")
    
    features_df = pd.read_csv(features_csv, index_col=0)
    
    # Train the GMM model
    gmm_model = train_gmm(features_df)
    
    # Optionally, print some details about the model:
    print("Trained GMM Model:")
    print(gmm_model)
    
    # Save the model in the /models directory
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "gmm_model.pkl")
    save_model(gmm_model, model_path)

if __name__ == "__main__":
    main()