# MMS Data Analysis Project Documentation

## Project Overview
This project implements a machine learning pipeline for analyzing Magnetospheric Multiscale (MMS) spacecraft data using Gaussian Mixture Models (GMM). The pipeline processes ion spectrogram data to identify and classify different plasma regions in the magnetosphere.

## Pipeline Components

### 1. Data Loading (`read_cdf.py`)
- Reads MMS spacecraft data from CDF (Common Data Format) files
- Extracts ion spectrogram data and timestamps
- Resamples the data to 1-minute intervals for analysis
- Uses spacepy.pycdf for handling CDF files

### 2. Feature Engineering (`feature_engineering.py`)
Processes ion spectrogram data to extract three key features:

#### Features:
- **ratio_max_width**: Measures peak characteristics in the energy spectrum
- **ratio_high_low**: Compares high-energy (>4000 eV) to low-energy (<100 eV) intensities
- **norm_Bt**: Normalizes the total magnetic field to 50 nT

#### Pseudofeature Implementation:
- Zeros all features if:
  - High-energy spectrum shows strong linear correlation (r > 0.7)
  - No valid peaks are detected
- Saves processed features to CSV format

### 3. Visualization (`vis_v3.py`)
Creates visual representations of the GMM clustering results:
- Loads processed features and trained GMM model
- Generates 2D scatter plots of the first two features
- Visualizes GMM clusters using:
  - Color-coded cluster assignments
  - Ellipses showing Gaussian distributions (2σ)
  - Clear labels and legends

## Data Processing Flow
1. Raw CDF data → read_cdf.py
2. Resampled time series → feature_engineering.py
3. Extracted features → GMM model
4. Cluster assignments → Visualization

## Dependencies
- Python 3.9
- spacepy
- numpy
- pandas
- scikit-learn
- matplotlib
- joblib

## Project Structure 

```
gaussian_mixed_model_mms/
├── data/
│   ├── processed/
│   └── raw/
├── models/
│   └── gmm_v1.py
├── scripts/
│   ├── feature_engineering.py
│   └── read_cdf.py
├── visualizations/
│   ├── vis_v1.py
│   ├── vis_v2.py
│   └── vis_v3.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gaussian_mixed_model_mms.git
   cd gaussian_mixed_model_mms
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Using Docker:
   ```bash
   docker build -t gaussian_mixed_model_mms .
   docker run -v $(pwd)/data:/gaussian_mixed_model_mms/data gaussian_mixed_model_mms
   ```

## Usage
1. Place raw CDF files in the data/raw directory
2. Run the scripts in order:
   ```bash
   python scripts/read_cdf.py
   python scripts/feature_engineering.py
   python visualization/vis_v3.py
   ```

## Output
- Processed features are saved in `data/processed/features.csv`
- GMM model is saved in `models/gmm_model.pkl`
- Visualization plots show cluster assignments and Gaussian components

## Notes
- The project is designed for MMS ion spectrogram analysis
- Features are carefully chosen to identify plasma regions
- Visualization helps in understanding the clustering results
