import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import sys
import os

def remove_outliers(data_series, z_threshold=2.0):
    """
    Removes data points that are further than 'z_threshold' 
    standard deviations away from the mean.
    """
    z_scores = np.abs(stats.zscore(data_series))
    filtered_data = data_series[z_scores < z_threshold]
    
    # Calculate how many spikes we removed for the log
    removed_count = len(data_series) - len(filtered_data)
    return filtered_data, removed_count

def compare_energy(baseline_csv, optimized_csv):
    try:
        # Load the raw data
        raw_base = pd.read_csv(baseline_csv, sep=';')['package_0'] / 1_000_000
        raw_opt = pd.read_csv(optimized_csv, sep=';')['package_0'] / 1_000_000
        
        # Apply the Z-Score filter (removing runs outside 2 Standard Deviations)
        base_data, base_dropped = remove_outliers(raw_base, z_threshold=2.0)
        opt_data, opt_dropped = remove_outliers(raw_opt, z_threshold=2.0)
        
        # Calculate clean statistics
        base_mean, base_std = base_data.mean(), base_data.std()
        opt_mean, opt_std = opt_data.mean(), opt_data.std()
        
        energy_saved = base_mean - opt_mean
        percent_saved = (energy_saved / base_mean) * 100
        
        # Perform Welch's t-test on the clean data
        t_stat, p_val = stats.ttest_ind(base_data, opt_data, equal_var=False)
        
        print("\n=== GREEN SOFTWARE RESULTS (FILTERED) ===")
        print(f"Data Cleaning:  Removed {base_dropped} baseline outliers and {opt_dropped} baseline_2 outliers.")
        print(f"Baseline Mean:  {base_mean:.2f} J")
        print(f"Baseline_2 Mean: {opt_mean:.2f} J")
        print(f"Energy Saved:   {energy_saved:.2f} J per run ({percent_saved:.2f}%)")
        print(f"P-Value:        {p_val:.4e}")
        
        if p_val < 0.05:
            print("Conclusion: The optimization is STATISTICALLY SIGNIFICANT.")
        else:
            print("Conclusion: The optimization is NOT statistically significant (noise).")
            
        # --- Plotting the Visual Proof ---
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.figure(figsize=(8, 5))
        plt.gca().set_facecolor('white')
        
        # Plot Baseline
        plt.hist(base_data, bins=8, density=True, alpha=0.5, color='#d62728', label='Baseline (Filtered)')
        x_base = np.linspace(base_mean - 3*base_std, base_mean + 3*base_std, 100)
        plt.plot(x_base, stats.norm.pdf(x_base, base_mean, base_std), color='#d62728', linewidth=2)
        
        # Plot Optimized
        plt.hist(opt_data, bins=8, density=True, alpha=0.5, color='#2ca02c', label='Optimized (Filtered)')
        x_opt = np.linspace(opt_mean - 3*opt_std, opt_mean + 3*opt_std, 100)
        plt.plot(x_opt, stats.norm.pdf(x_opt, opt_mean, opt_std), color='#2ca02c', linewidth=2)
        
        # Add Mean Lines
        plt.axvline(base_mean, color='#d62728', linestyle='dashed', linewidth=1.5)
        plt.axvline(opt_mean, color='#2ca02c', linestyle='dashed', linewidth=1.5)
        
        plt.title('Energy Reduction (Outliers Removed)', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('CPU Package Energy Consumed (Joules)', fontsize=12)
        plt.yticks([]) 
        plt.legend(frameon=True, fontsize=11)
        
        for spine in ['top', 'right', 'left']:
            plt.gca().spines[spine].set_visible(False)
            
        plt.tight_layout()
        
        # Save output in the root green_metrics folder for easy access
        output_name = 'energy_comparison_plot.pdf'
        plt.savefig(output_name, format='pdf', bbox_inches='tight')
        print(f"\nSuccess: Generated '{output_name}'")

    except FileNotFoundError as e:
        print(f"Error: Could not find one of the CSV files. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # If paths are provided via CLI, use them. Otherwise, default to these specific experiment folders.
    base_path = sys.argv[1] if len(sys.argv) > 1 else 'experiments/baseline/raw_energy_data.csv'
    opt_path = sys.argv[2] if len(sys.argv) > 2 else 'experiments/baseline_2/raw_energy_data.csv'
    
    compare_energy(base_path, opt_path)