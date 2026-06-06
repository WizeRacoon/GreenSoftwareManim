from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import subprocess

# Set up a CSV to store the data
csv_handler = CSVHandler('baseline_energy.csv')

@measure_energy(handler=csv_handler)
def render_scene():
    # Renders high quality (-qh) with no caching to ensure maximum CPU load
    subprocess.run(["manim", "-qh", "--disable_caching", "my_scenes.py", "HeavyScene"], check=True)

if __name__ == "__main__":
    NUM_RUNS = 30
    print(f"Starting {NUM_RUNS} benchmark runs for statistical significance...")
    
    for i in range(NUM_RUNS):
        print(f"Run {i+1} of {NUM_RUNS}...")
        render_scene()
        
    csv_handler.save_data()
    print("Done! Data saved to baseline_energy.csv")