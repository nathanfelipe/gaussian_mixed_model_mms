#!/usr/bin/env python3
"""
feature_engineering.py

This module extracts features from 1‐minute averaged ion spectrogram data
and the total magnetic field magnitude (Btot) according to the methodology
described in the research article. The extracted features are:

  - ratio_max_width: Ratio between the computed peak width and the number of energy channels.
  - ratio_high_low:  Ratio of the mean log intensity for energies >4000 eV to those <100 eV.
  - norm_Bt:       Btot normalized to 50 nT (values above 50 nT become 1).

A pseudofeature is also implemented: if the linear fit (via Pearson correlation) to the
high‐energy (>300 eV) half of the spectrum yields r > 0.7—or if no valid peak is detected—
the other features are set to zero.
"""

import os
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, peak_widths
from scipy.stats import pearsonr

def compute_peak_features(log_counts, num_channels=32):
    """
    Identify peaks in the log-transformed ion spectrum using SciPy's find_peaks,
    then compute ratio_max_width based on the most prominent peak.
    
    Parameters:
        log_counts (np.array): 1D array of log-transformed ion spectrogram counts.
        num_channels (int):  Number of energy channels (default is 32).
    
    Returns:
        ratio_max_width (float or None): Computed ratio_max_width or None if no peak is found.
    """
    # Use find_peaks with parameters: width=1, height=1, prominence=0.2
    peaks, properties = find_peaks(log_counts, height=1, prominence=0.2, width=1)
    if len(peaks) == 0:
        return None  # No peak detected.
    
    # Select the peak with the maximum height (i.e. the global maximum)
    peak_heights = properties['peak_heights']
    max_idx = np.argmax(peak_heights)
    max_peak = peaks[max_idx]
    
    # Compute peak widths using peak_widths
    widths, width_heights, left_ips, right_ips = peak_widths(log_counts, [max_peak], rel_height=0.5)
    
    # Define width as twice the distance between the left intersection and the peak index.
    computed_width = 2 * (max_peak - left_ips[0])
    ratio_max_width = computed_width / num_channels
    return ratio_max_width

def compute_ratio_high_low(log_counts, energy_bins):
    """
    Compute ratio_high_low as the ratio of the mean log intensity for channels with energy >4000 eV
    to the mean log intensity for channels with energy <100 eV.
    
    Parameters:
        log_counts (np.array): 1D array of log-transformed ion spectrogram counts.
        energy_bins (np.array): 1D array of energy values corresponding to each channel.
        
    Returns:
        ratio (float or None): The computed ratio_high_low. Returns None if the required channels are not available.
    """
    high_mask = energy_bins > 4000
    low_mask = energy_bins < 100
    
    if not np.any(high_mask) or not np.any(low_mask):
        return None  # One of the groups is missing.
    
    high_mean = np.mean(log_counts[high_mask])
    low_mean = np.mean(log_counts[low_mask])
    
    # Avoid division by zero
    if low_mean == 0:
        return None
    
    return high_mean / low_mean

def compute_norm_Bt(Btot):
    """
    Compute norm_Bt by normalizing Btot to 50 nT. Any Btot value above 50 nT is set to 1.
    
    Parameters:
        Btot (float): Total magnetic field magnitude in nT.
    
    Returns:
        norm_Bt (float): Normalized Btot.
    """
    normalized = Btot / 50.0
    return normalized if normalized <= 1 else 1

def check_pseudofeature(log_counts, energy_bins):
    """
    Evaluate the pseudofeature condition by fitting a linear relationship
    (using the Pearson correlation) to the high-energy (>300 eV) portion of the spectrum.
    
    Parameters:
        log_counts (np.array): 1D array of log-transformed ion spectrogram counts.
        energy_bins (np.array): 1D array of energy values corresponding to each channel.
        
    Returns:
        trigger (bool): True if the Pearson correlation coefficient exceeds 0.7 or if there are insufficient data,
                        indicating that the pseudofeature condition is met.
    """
    mask = energy_bins > 300
    if not np.any(mask):
        return True  # No high-energy channels; trigger pseudofeature.
    
    x = energy_bins[mask]
    y = log_counts[mask]
    
    if len(x) < 2:
        return True  # Not enough points for a meaningful regression.
    
    r, _ = pearsonr(x, y)
    return r > 0.7

def process_spectrum(spectrum, Btot, energy_bins, num_channels=32):
    """
    Process a single 1-minute averaged ion spectrum to compute the three features.
    
    The function:
      - Converts the raw spectrum to log counts.
      - Computes ratio_max_width via peak detection.
      - Computes ratio_high_low using energy thresholds.
      - Computes norm_Bt using the provided Btot value.
      - Checks the pseudofeature condition: if triggered (or if no peak is detected),
        all three features are set to zero.
    
    Parameters:
        spectrum (np.array): 1D array of ion spectrogram counts for one time bin.
        Btot (float): Total magnetic field magnitude for the corresponding time bin.
        energy_bins (np.array): 1D array of energy values for each channel.
        num_channels (int): Number of energy channels (default is 32).
    
    Returns:
        features (dict): Dictionary containing 'ratio_max_width', 'ratio_high_low', and 'norm_Bt'.
    """
    # Avoid taking log of zero by adding a very small constant
    log_counts = np.log10(spectrum + 1e-6)
    
    # Compute the peak-based feature.
    ratio_max_width = compute_peak_features(log_counts, num_channels)
    
    # If no peak is detected, we treat this as a trigger for the pseudofeature.
    pseudofeature_triggered = (ratio_max_width is None)
    
    # Compute ratio_high_low.
    ratio_high_low = compute_ratio_high_low(log_counts, energy_bins)
    if ratio_high_low is None:
        pseudofeature_triggered = True
    
    # Compute normalized Btot.
    norm_Bt = compute_norm_Bt(Btot)
    
    # Check pseudofeature condition via linear fit on high-energy channels.
    if not pseudofeature_triggered:
        pseudofeature_triggered = check_pseudofeature(log_counts, energy_bins)
    
    # If the pseudofeature condition is met, set all three features to zero.
    if pseudofeature_triggered:
        ratio_max_width = 0
        ratio_high_low = 0
        norm_Bt = 0
    
    features = {
        'ratio_max_width': ratio_max_width,
        'ratio_high_low': ratio_high_low,
        'norm_Bt': norm_Bt
    }
    return features

def process_all_spectra(ion_spec_df, Btot_series, energy_bins):
    """
    Process all 1-minute averaged ion spectra to extract features.
    
    Parameters:
        ion_spec_df (pd.DataFrame): DataFrame containing resampled ion spectrogram data.
                                    Each row corresponds to one 1-minute time bin and has 32 channels.
        Btot_series (pd.Series): Series containing the total magnetic field magnitude for each 1-minute bin.
        energy_bins (np.array): 1D array of energy values corresponding to the 32 channels.
    
    Returns:
        features_df (pd.DataFrame): DataFrame with the computed features for each time bin.
    """
    feature_list = []
    for timestamp, row in ion_spec_df.iterrows():
        spectrum = row.values
        # Assumes the time indices align between the ion spectrum and the Btot data.
        Btot = Btot_series.loc[timestamp] if timestamp in Btot_series.index else np.nan
        features = process_spectrum(spectrum, Btot, energy_bins)
        feature_list.append(features)
    
    features_df = pd.DataFrame(feature_list, index=ion_spec_df.index)
    
    # Export features to CSV
    output_path = 'data/processed/features.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Create directory if it doesn't exist
    features_df.to_csv(output_path)
    print(f"Features exported to: {output_path}")
    
    return features_df

if __name__ == "__main__":
    # Example usage / test run:
    # Create an energy_bins array (assuming 32 channels from 10 eV to 30 keV, logarithmically spaced)
    energy_bins = np.logspace(np.log10(10), np.log10(30000), 32)
    
    # For demonstration, create dummy data for 65 1-minute bins.
    dates = pd.date_range("2015-10-17 04:55", periods=65, freq="1Min")
    # Simulated ion spectrogram counts (e.g., could be in units of log counts)
    ion_spec_dummy = np.random.rand(65, 32) * 1e6  
    # Simulated total magnetic field magnitude values between 0 and 100 nT.
    Btot_dummy = pd.Series(np.random.rand(65) * 100, index=dates)
    ion_spec_df_dummy = pd.DataFrame(ion_spec_dummy, index=dates)
    
    # Process the dummy spectra to extract features.
    features_df = process_all_spectra(ion_spec_df_dummy, Btot_dummy, energy_bins)
    print("Extracted Features (first 5 rows):")
    print(features_df.head())