import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import sys
import os

def remove_outliers(data_series, threshold=3.0):
    """
    Uses Median Absolute Deviation (MAD) to calculate a Robust Z-Score.
    Completely immune to outlier masking from extreme hardware spikes.
    """
    median = data_series.median()
    abs_deviation = np.abs(data_series - median)
    mad = abs_deviation.median()
    
    if mad == 0:
        return data_series, 0
        
    robust_z_scores = 0.6745 * abs_deviation / mad
    filtered_data = data_series[robust_z_scores < threshold]
    removed_count = len(data_series) - len(filtered_data)
    
    return filtered_data, removed_count

def compare_energy(exp1_name, exp2_name):
    # --- ABSOLUTE PATH ROUTING ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "experiments", exp1_name, "raw_energy_data.csv")
    opt_path = os.path.join(script_dir, "experiments", exp2_name, "raw_energy_data.csv")
    
    try:
        # Load the raw data
        raw_base = pd.read_csv(base_path, sep=';')['package_0'] / 1_000_000
        raw_opt = pd.read_csv(opt_path, sep=';')['package_0'] / 1_000_000
        
        # --- THE FIX: Pass 'threshold' instead of 'z_threshold' ---
        base_data, base_dropped = remove_outliers(raw_base, threshold=3.0)
        opt_data, opt_dropped = remove_outliers(raw_opt, threshold=3.0)
        
        # Calculate clean statistics
        base_mean, base_std = base_data.mean(), base_data.std()
        opt_mean, opt_std = opt_data.mean(), opt_data.std()
        
        energy_saved = base_mean - opt_mean
        percent_saved = (energy_saved / base_mean) * 100
        
        # Perform Welch's t-test on the clean data
        t_stat, p_val = stats.ttest_ind(base_data, opt_data, equal_var=False)
        
        print("\n=== GREEN SOFTWARE RESULTS (MAD FILTERED) ===")
        print(f"Comparing:      {exp1_name} vs {exp2_name}")
        print(f"Data Cleaning:  Removed {base_dropped} outliers from {exp1_name} and {opt_dropped} from {exp2_name}.")
        print(f"{exp1_name} Mean: {base_mean:.2f} J")
        print(f"{exp2_name} Mean: {opt_mean:.2f} J")
        print(f"Difference:     {energy_saved:.2f} J per run ({percent_saved:.2f}%)")
        print(f"P-Value:        {p_val:.4e}")
        
        if p_val < 0.05:
            print("Conclusion: The difference is STATISTICALLY SIGNIFICANT.")
            significance_text = "Statistically Significant"
        else:
            print("Conclusion: The difference is NOT statistically significant (noise).")
            significance_text = "Not Statistically Significant"
            
        # --- Plotting the Visual Proof ---
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.figure(figsize=(9, 5.5))
        plt.gca().set_facecolor('white')
        
        # Plot Experiment 1 (Red)
        plt.hist(base_data, bins=8, density=True, alpha=0.5, color='#d62728', label=f'{exp1_name} (Filtered)')
        x_base = np.linspace(base_mean - 3*base_std, base_mean + 3*base_std, 100)
        plt.plot(x_base, stats.norm.pdf(x_base, base_mean, base_std), color='#d62728', linewidth=2)
        
        # Plot Experiment 2 (Green)
        plt.hist(opt_data, bins=8, density=True, alpha=0.5, color='#2ca02c', label=f'{exp2_name} (Filtered)')
        x_opt = np.linspace(opt_mean - 3*opt_std, opt_mean + 3*opt_std, 100)
        plt.plot(x_opt, stats.norm.pdf(x_opt, opt_mean, opt_std), color='#2ca02c', linewidth=2)
        
        # Add Mean Lines
        plt.axvline(base_mean, color='#d62728', linestyle='dashed', linewidth=2, 
                    label=f'{exp1_name} Mean: {base_mean:.1f} J')
        plt.axvline(opt_mean, color='#2ca02c', linestyle='dashed', linewidth=2, 
                    label=f'{exp2_name} Mean: {opt_mean:.1f} J')
        
        # Dynamic P-Value formatting
        if p_val < 0.001:
            p_string = f"p = {p_val:.3e}"
        else:
            p_string = f"p = {p_val:.3f}"
            
        plt.title(f'Energy Comparison: {exp1_name} vs {exp2_name}', fontsize=14, fontweight='bold', pad=20)
        plt.figtext(0.5, 0.90, f'Welch\'s t-test: {p_string} ({significance_text})', 
                    fontsize=11, fontstyle='italic', ha='center', color='#444444')
        
        plt.xlabel('CPU Package Energy Consumed (Joules)', fontsize=12)
        plt.yticks([]) 
        plt.legend(loc='upper right', frameon=True, fontsize=11)
        
        for spine in ['top', 'right', 'left']:
            plt.gca().spines[spine].set_visible(False)
            
        plt.tight_layout()
        
        output_name = f'{exp1_name}_vs_{exp2_name}.pdf'
        output_path = os.path.join(script_dir, output_name)
        
        plt.savefig(output_path, format='pdf', bbox_inches='tight')
        print(f"\nSuccess: Generated '{output_path}'")

    except FileNotFoundError as e:
        print(f"\nError: Could not find one of the CSV files.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 compare_energy.py [experiment_1] [experiment_2]")
        sys.exit(1)
        
    exp_1 = sys.argv[1]
    exp_2 = sys.argv[2]
    
    compare_energy(exp_1, exp_2)