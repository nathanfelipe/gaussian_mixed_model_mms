from spacepy import pycdf
import numpy as np
import pandas as pd
import glob
import os

def load_cdf_files(data_dir):
    """
    Load and concatenate multiple CDF files from a directory. Still missing to download cdfs
    containig the B field data. Possibly FGM (Fluxgate Magnetometer) data.
    
    Parameters:
        data_dir (str): Path to directory containing CDF files
        
    Returns:
        tuple: (ion_spec_df, B_field_df) - Resampled DataFrames for ion spectrogram and magnetic field
    """
    # Get list of all CDF files in directory
    cdf_files = glob.glob(os.path.join(data_dir, '*.cdf'))
    
    # Lists to store DataFrames from each file
    ion_spec_list = []
    B_field_list = []
    
    for cdf_file in sorted(cdf_files):
        try:
            # Open the CDF file
            with pycdf.CDF(cdf_file) as cdf:
                # Extract the epoch and ion spectrogram data
                epoch = cdf['Epoch'][:]
                ion_spec = cdf['mms1_dis_energyspectr_px_fast'][:]
                
                # Extract magnetic field data
                B_field = cdf['mms1_fgm_b_gse_brst_l2'][:]  # Adjust variable name if needed
                
                # Create DataFrames for this file
                ion_df = pd.DataFrame(ion_spec, index=pd.to_datetime(epoch))
                
                # For B field, calculate the magnitude (Btot)
                Btot = np.sqrt(np.sum(B_field[:, :3]**2, axis=1))  # Using only x,y,z components
                B_df = pd.DataFrame({'Btot': Btot}, index=pd.to_datetime(epoch))
                
                ion_spec_list.append(ion_df)
                B_field_list.append(B_df)
                
                print(f"Loaded: {os.path.basename(cdf_file)}")
                
        except Exception as e:
            print(f"Error loading {cdf_file}: {str(e)}")
    
    # Concatenate all DataFrames
    if ion_spec_list and B_field_list:
        # Combine ion spectrogram data
        ion_spec_df = pd.concat(ion_spec_list, axis=0)
        ion_spec_df = ion_spec_df.sort_index()
        ion_spec_df = ion_spec_df[~ion_spec_df.index.duplicated(keep='first')]
        
        # Combine B field data
        B_field_df = pd.concat(B_field_list, axis=0)
        B_field_df = B_field_df.sort_index()
        B_field_df = B_field_df[~B_field_df.index.duplicated(keep='first')]
        
        # Resample both to 1-minute intervals
        ion_spec_resampled = ion_spec_df.resample('1Min').mean()
        B_field_resampled = B_field_df.resample('1Min').mean()
        
        print("\nFinal Dataset:")
        print(f"Time range: {ion_spec_resampled.index[0]} to {ion_spec_resampled.index[-1]}")
        print(f"Total samples: {len(ion_spec_resampled)}")
        
        return ion_spec_resampled, B_field_resampled
    else:
        raise ValueError("No valid CDF files were loaded")

if __name__ == "__main__":
    # Specify your data directory
    data_dir = '/Users/nathan/CursorProjects/gaussian_mixed_model_mms/data'
    
    # Load and process all CDF files
    ion_spec_df, B_field_df = load_cdf_files(data_dir)
    
    # Save the concatenated and resampled data
    output_dir = 'data/processed'
    os.makedirs(output_dir, exist_ok=True)
    
    ion_spec_df.to_csv(os.path.join(output_dir, 'concatenated_ion_spec.csv'))
    B_field_df.to_csv(os.path.join(output_dir, 'concatenated_B_field.csv'))
    
    print(f"\nSaved concatenated data to: {output_dir}")