from spacepy import pycdf
import numpy as np
import pandas as pd

# Open the CDF file (read-only mode)
cdf_file = '/Users/nathan/CursorProjects/gus_first_project /data/mms1_fpi_fast_l2_dis-moms_20151017040000_v3.4.0.cdf'
cdf = pycdf.CDF(cdf_file)

# Extract the epoch and ion spectrogram data
epoch = cdf['Epoch'][:]  # array of datetime.datetime objects, shape (439,)
ion_spec = cdf['mms1_dis_energyspectr_px_fast'][:]  # NumPy array, shape (439, 32)

# Don't forget to close the CDF file when done
cdf.close()

# Create a DataFrame with the ion spectrogram data and the epoch as the index
ion_spec_df = pd.DataFrame(ion_spec, index=pd.to_datetime(epoch))

# Check the index to confirm it is in datetime format
print(ion_spec_df.index)

# Resample the data: Group all data points in each 1-minute window and compute their mean
df_resampled = ion_spec_df.resample('1Min').mean()

# Inspect the resampled DataFrame
print("Resampled Ion Spectrogram Data:")
print(df_resampled.head())
print("Resampled data shape:", df_resampled.shape)