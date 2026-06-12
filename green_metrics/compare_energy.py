import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import sys
import os

def remove_outliers(data_series, threshold=3.0):
    """
    Uses Median Absolute Deviation (MAD) to calculate a Robust Z-Score.
    Immune to outlier masking from extreme hardware spikes.
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
    processed_data = []
    colors = ['#d62728', '#2ca02c', '#1f77b4', '#9467bd', '#ff7f0e', '#8c564b']
    
    try:
        # --- 1. Load and Clean All Data ---
        # Your measured baseline idle power (Watts)
        IDLE_POWER_WATTS = 20.6581 
        
        for exp_name in experiments:
            raw_path = os.path.join(script_dir, "experiments", exp_name, "raw_energy_data.csv")
            
            # Load the complete dataframe to cross-reference energy against time
            raw_df = pd.read_csv(raw_path, sep=';')
            
            # 1. Convert raw micro-joules to standard Joules
            measured_energy = raw_df['package_0'] / 1_000_000
            duration_seconds = raw_df['duration']
            
            # 2. Consequential Isolation: Subtract baseline background leakage
            isolated_energy = measured_energy - (IDLE_POWER_WATTS * duration_seconds)
            
            # Run your MAD outlier cleanup on the cleanly isolated data plane
            clean_data, dropped = remove_outliers(isolated_energy, threshold=3.0)
            mean, std = clean_data.mean(), clean_data.std()
            
            processed_data.append({
                'name': exp_name,
                'data': clean_data,
                'mean': mean,
                'std': std,
                'dropped': dropped,
                'p_val': None,
                'significant': None
            })
        
        baseline = processed_data[0]
        
        # --- 2. Print Statistical Comparisons & Store Significance ---
        print(f"\n=== GREEN SOFTWARE RESULTS (MAD FILTERED) ===")
        print(f"Baseline Experiment: {baseline['name']}")
        print(f"Baseline Mean:       {baseline['mean']:.2f} J (Removed {baseline['dropped']} outliers)")
        print("-" * 65)
        
        for i, exp in enumerate(processed_data[1:], start=1):
            # Compute Welch's t-test
            t_stat, p_val = stats.ttest_ind(baseline['data'], exp['data'], equal_var=False)
            exp['p_val'] = p_val
            exp['significant'] = p_val < 0.05
            
            energy_saved = baseline['mean'] - exp['mean']
            percent_saved = (energy_saved / baseline['mean']) * 100
            sig_text = "SIGNIFICANT" if exp['significant'] else "NOISE"
            
            print(f"Comparison {i}:       {exp['name']}")
            print(f"Mean:             {exp['mean']:.2f} J (Removed {exp['dropped']} outliers)")
            print(f"Savings:          {energy_saved:.2f} J per run ({percent_saved:.2f}%)")
            print(f"P-Value:          {p_val:.4e} -> [{sig_text}]")
            print("-" * 65)

        # --- 3. Plotting the Visual Proof with Significance Markers ---
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.figure(figsize=(11, 6))  # Widened slightly to prevent legend overlapping data
        plt.gca().set_facecolor('white')
        
        # Plot each experiment dynamically
        for idx, exp in enumerate(processed_data):
            color = colors[idx % len(colors)]
            
            # Plot Histogram
            plt.hist(exp['data'], bins=10, density=True, alpha=0.20, color=color)
            
            # Plot Normal Distribution Curve
            x_range = np.linspace(exp['mean'] - 3*exp['std'], exp['mean'] + 3*exp['std'], 100)
            plt.plot(x_range, stats.norm.pdf(x_range, exp['mean'], exp['std']), color=color, linewidth=2)
            
            # --- Dynamic Legend Label Generation ---
            if idx == 0:
                # Baseline identifier label
                label_text = f"{exp['name']} ({exp['mean']:.2f} J) [Baseline]"
            else:
                # Append p-value and context text to optimization labels
                p_val = exp['p_val']
                p_string = f"p={p_val:.3e}" if p_val < 0.001 else f"p={p_val:.3f}"
                sig_string = "Significant" if exp['significant'] else "Noise"
                label_text = f"{exp['name']} ({exp['mean']:.2f} J) [{p_string}, {sig_string}]"
            
            # Add Vertical Mean Line using the compiled label text
            plt.axvline(exp['mean'], color=color, linestyle='dashed', linewidth=2, label=label_text)

        plt.title('Energy Comparison: Ablation Study', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('CPU Package Energy Consumed (Joules)', fontsize=12)
        plt.yticks([]) 
        
        # Display the descriptive statistical legend box
        plt.legend(loc='upper right', frameon=True, fontsize=9.5, facecolor='white', edgecolor='#e0e0e0')
        
        for spine in ['top', 'right', 'left']:
            plt.gca().spines[spine].set_visible(False)
            
        plt.tight_layout()
        
        # --- 4. Export the Output ---
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
    if len(sys.argv) < 3:
        print("Usage: python3 compare_energy.py [baseline_experiment] [exp_2] [exp_3] ...")
        sys.exit(1)
        
    experiment_list = sys.argv[1:]
    compare_energy(experiment_list)