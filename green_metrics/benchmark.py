from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import subprocess
import sys

# Set up a CSV to store the data
csv_handler = CSVHandler('baseline_energy.csv')

@measure_energy(handler=csv_handler)
def render_scene():
    subprocess.run(["manim", "-qh", "--disable_caching", "my_scenes.py", "HeavyScene"], check=True)

if __name__ == "__main__":
    # Grab the argument from the bash script, defaulting to 50 if omitted
    NUM_RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    
    print(f"Starting {NUM_RUNS} benchmark runs for statistical significance...")
    
    for i in range(NUM_RUNS):
        print(f"Run {i+1} of {NUM_RUNS}...")
        render_scene()
        
    csv_handler.save_data()
    print("Done! Data saved to baseline_energy.csv")