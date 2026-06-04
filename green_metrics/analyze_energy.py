import pandas as pd

def calculate_statistics(csv_file):
    try:
        # pyJoules uses a semicolon separator by default
        df = pd.read_csv(csv_file, sep=';')
        
        # Find the columns that contain the actual energy readings
        # Typical pyJoules column names: package_0, core_0, uncore_0
        energy_cols = [col for col in df.columns if 'package' in col or 'core' in col]
        
        print(f"--- Energy Statistics ({len(df)} runs) ---")
        
        for col in energy_cols:
            # Convert microjoules to Joules for the final report
            data_in_joules = df[col] / 1_000_000
            
            mean_val = data_in_joules.mean()
            std_dev = data_in_joules.std()
            variance = data_in_joules.var()
            
            print(f"\nTarget Metric: {col}")
            print(f"  Mean:     {mean_val:.4f} Joules")
            print(f"  Std Dev:  {std_dev:.4f} Joules")
            print(f"  Variance: {variance:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Run the benchmark loop first!")
    except Exception as e:
        print(f"An error occurred while parsing the data: {e}")

if __name__ == "__main__":
    calculate_statistics('baseline_energy.csv')