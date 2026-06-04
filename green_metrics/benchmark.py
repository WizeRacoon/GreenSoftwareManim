from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import subprocess

# Set up a CSV to store the data
csv_handler = CSVHandler('baseline_energy.csv')

@measure_energy(handler=csv_handler)
def render_scene():
    # Replace 'my_scenes.py' and 'HeavyScene' with your chosen benchmarks
    # The '-qh' flag renders at lower quality for faster iterations during testing, 
    # but you should use '-qh' (high quality) for your final data gathering.
    subprocess.run(["manim", "-qh", "--disable_caching", "my_scenes.py", "HeavyScene"], check=True)

if __name__ == "__main__":
    render_scene()
    csv_handler.save_data()