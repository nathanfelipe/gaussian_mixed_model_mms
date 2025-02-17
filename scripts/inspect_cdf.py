from spacepy import pycdf
import os
import sys
from datetime import datetime

def inspect_cdf_file(file_path, output_file):
    """
    Inspect the contents of a CDF file and write information about its variables to a file
    
    Parameters:
        file_path (str): Path to the CDF file
        output_file (file): File object to write output to
    """
    output_file.write(f"\nInspecting: {os.path.basename(file_path)}\n")
    output_file.write("-" * 80 + "\n")
    
    with pycdf.CDF(file_path) as cdf:
        # Get list of variables
        variables = cdf.keys()
        
        output_file.write("Available variables:\n")
        output_file.write("-" * 80 + "\n")
        
        for var in variables:
            try:
                # Get variable info
                data = cdf[var]
                shape = data.shape if hasattr(data, 'shape') else 'scalar'
                
                # Get attributes for this variable
                attrs = cdf[var].attrs
                
                output_file.write(f"\nVariable: {var}\n")
                output_file.write(f"Shape: {shape}\n")
                output_file.write("Attributes:\n")
                for attr, value in attrs.items():
                    output_file.write(f"  {attr}: {value}\n")
                
            except Exception as e:
                output_file.write(f"Error reading {var}: {str(e)}\n")
        
        output_file.write("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = 'data/cdf_inspection'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create output file with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f'cdf_inspection_{timestamp}.txt')
    
    # Specify path to CDF files
    data_dir = '/Users/nathan/CursorProjects/gaussian_mixed_model_mms/data'
    
    # Get list of CDF files
    cdf_files = [f for f in os.listdir(data_dir) if f.endswith('.cdf')]
    
    with open(output_path, 'w') as output_file:
        # Write header
        output_file.write("CDF File Inspection Report\n")
        output_file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output_file.write("=" * 80 + "\n")
        
        if cdf_files:
            for cdf_file in cdf_files:
                file_path = os.path.join(data_dir, cdf_file)
                inspect_cdf_file(file_path, output_file)
            print(f"Inspection report saved to: {output_path}")
        else:
            output_file.write("\nNo CDF files found in directory\n")
            print("No CDF files found in directory") 