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

def compare_energy(experiments):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Store processed data for all experiments
    processed_data = []
    
    # Color palette for up to 6 simultaneous experiments
    colors = ['#d62728', '#2ca02c', '#1f77b4', '#9467bd', '#ff7f0e', '#8c564b']
    
    try:
        # --- 1. Load and Clean All Data ---
        for exp_name in experiments:
            raw_path = os.path.join(script_dir, "experiments", exp_name, "raw_energy_data.csv")
            raw_data = pd.read_csv(raw_path, sep=';')['package_0'] / 1_000_000
            
            clean_data, dropped = remove_outliers(raw_data, threshold=3.0)
            mean, std = clean_data.mean(), clean_data.std()
            
            processed_data.append({
                'name': exp_name,
                'data': clean_data,
                'mean': mean,
                'std': std,
                'dropped': dropped
            })
            
        baseline = processed_data[0]
        
        # --- 2. Print Statistical Comparisons ---
        print(f"\n=== GREEN SOFTWARE RESULTS (MAD FILTERED) ===")
        print(f"Baseline Experiment: {baseline['name']}")
        print(f"Baseline Mean:       {baseline['mean']:.2f} J (Removed {baseline['dropped']} outliers)")
        print("-" * 55)
        
        for i, exp in enumerate(processed_data[1:], start=1):
            energy_saved = baseline['mean'] - exp['mean']
            percent_saved = (energy_saved / baseline['mean']) * 100
            t_stat, p_val = stats.ttest_ind(baseline['data'], exp['data'], equal_var=False)
            
            sig_text = "SIGNIFICANT" if p_val < 0.05 else "NOISE"
            
            print(f"Comparison {i}:       {exp['name']}")
            print(f"Mean:             {exp['mean']:.2f} J (Removed {exp['dropped']} outliers)")
            print(f"Savings:          {energy_saved:.2f} J per run ({percent_saved:.2f}%)")
            print(f"P-Value:          {p_val:.4e} -> [{sig_text}]")
            print("-" * 55)

        # --- 3. Plotting the Visual Proof ---
        plt.style.use('seaborn-v0_8-whitegrid')
        # Make the chart slightly wider to accommodate a larger legend
        plt.figure(figsize=(10, 6))
        plt.gca().set_facecolor('white')
        
        # Plot each experiment dynamically
        for idx, exp in enumerate(processed_data):
            color = colors[idx % len(colors)]
            
            # Plot Histogram
            plt.hist(exp['data'], bins=8, density=True, alpha=0.35, color=color)
            
            # Plot Normal Distribution Curve
            x_range = np.linspace(exp['mean'] - 3*exp['std'], exp['mean'] + 3*exp['std'], 100)
            plt.plot(x_range, stats.norm.pdf(x_range, exp['mean'], exp['std']), color=color, linewidth=2)
            
            # Add Vertical Mean Line & Legend Label
            plt.axvline(exp['mean'], color=color, linestyle='dashed', linewidth=2, 
                        label=f"{exp['name']} ({exp['mean']:.2f} J)")

        plt.title(f'Energy Comparison: Ablation Study', fontsize=14, fontweight='bold', pad=15)
        
        plt.xlabel('CPU Package Energy Consumed (Joules)', fontsize=12)
        plt.yticks([]) 
        
        # Move legend outside the plot area if there are many experiments
        plt.legend(loc='upper right', frameon=True, fontsize=10)
        
        for spine in ['top', 'right', 'left']:
            plt.gca().spines[spine].set_visible(False)
            
        plt.tight_layout()
        
        # --- 4. Export the Output ---
        # Name the file based on the baseline and the number of comparisons
        output_name = f"{baseline['name']}_vs_{len(experiments)-1}_others.pdf"
        comparisons_dir = os.path.join(script_dir, "experiments", "comparisons")
        
        os.makedirs(comparisons_dir, exist_ok=True)
        output_path = os.path.join(comparisons_dir, output_name)
        
        plt.savefig(output_path, format='pdf', bbox_inches='tight')
        print(f"\nSuccess: Generated plot at '{output_path}'")

    except FileNotFoundError as e:
        print(f"\nError: Could not find one of the CSV files.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    # Ensure at least two experiments are provided
    if len(sys.argv) < 3:
        print("Usage: python3 compare_energy.py [baseline_experiment] [exp_2] [exp_3] ...")
        sys.exit(1)
        
    experiment_list = sys.argv[1:]
    compare_energy(experiment_list)