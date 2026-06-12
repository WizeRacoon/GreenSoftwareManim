#!/usr/bin/env python3
import time
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler

# Temporary handler to sample baseline idle states
csv_handler = CSVHandler('idle_baseline.csv')

@measure_energy(handler=csv_handler)
def sample_idle():
    # Sit completely idle for 30 seconds to capture pure background leakage
    time.sleep(30)

if __name__ == "__main__":
    print("Measuring system baseline idle power. Do not touch the PC...")
    sample_idle()
    csv_handler.save_data()
    
    # Read back the file to compute raw Watts (Joules / Seconds)
    import pandas as pd
    df = pd.read_csv('idle_baseline.csv', sep=';')
    total_joules = df['package_0'].iloc[0] / 1_000_000
    duration_seconds = df['duration'].iloc[0]
    
    idle_watts = total_joules / duration_seconds
    print(f"\nResulting Baseline Idle Power: {idle_watts:.4f} Watts (J/s)")