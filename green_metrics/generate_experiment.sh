#!/bin/bash

# Ensure the user provided an experiment name
if [ -z "$1" ]; then
    echo "🛑 Error: No experiment name provided."
    echo "Usage: ./generate_experiment.sh <experiment_name> [num_runs]"
    echo "Example: ./generate_experiment.sh 01_baseline 50"
    exit 1
fi

EXP_NAME=$1
# Dynamic Argument: Grab the second parameter ($2). If empty, default to 50.
NUM_RUNS=${2:-50}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXP_DIR="$SCRIPT_DIR/experiments/$EXP_NAME"

echo "================================================="
echo " 🧪 Initializing Experiment: $EXP_NAME ($NUM_RUNS runs)"
echo "================================================="

# Create the isolated experiment folder inside green_metrics/experiments/
mkdir -p "$EXP_DIR"

# ---------------------------------------------------------
# STAGE 1: The Safety Gateway
# ---------------------------------------------------------
echo -e "\n[1/6] 🛡️  Running Functionality & Safety Tests..."
python test_optimization.py

# The $? variable checks if the previous python script crashed or failed an assertion
if [ $? -ne 0 ]; then
    echo -e "\n❌ ABORT: Functionality test failed! The math or camera runtime is broken."
    echo "Fix the logic before running the energy benchmarks."
    # We delete the empty experiment folder so it doesn't clutter your workspace
    rm -r "$EXP_DIR" 
    exit 1
fi
echo "✅ Safety checks passed. Proceeding to physical benchmarks."

# ---------------------------------------------------------
# STAGE 2: Energy Benchmarking with Thermal Cooling
# ---------------------------------------------------------
echo -e "\n[2/6] ⚡ Running $NUM_RUNS isolated benchmarking loops..."

# Clear out any stale baseline data before starting
rm -f baseline_energy.csv

for ((i=1; i<=NUM_RUNS; i++)); do
    echo "🚀 Loop $i of $NUM_RUNS..."
    
    # taskset -c 3 forces it onto the hard-isolated core
    # We pass '1' to benchmark.py so it only executes exactly one render
    taskset -c 3 python benchmark.py 1
    
    # The Cooldown Phase: 7s to clear that thermal chattering boundary!
    if [ $i -lt $NUM_RUNS ]; then
        echo "💤 Cooling core for 7 seconds..."
        sleep 7
    fi
done

# ---------------------------------------------------------
# STAGE 3: Statistical Analysis
# ---------------------------------------------------------
echo -e "\n[3/6] 📊 Calculating Statistics..."
# Assuming analyze_energy.py generates energy_results_summary.txt
python analyze_energy.py 

# ---------------------------------------------------------
# STAGE 4: CPU Profiling
# ---------------------------------------------------------
echo -e "\n[4/6] ⏱️  Profiling CPU Time on Core 3..."
taskset -c 3 python -m cProfile -s tottime ../manim/__main__.py -qh --disable_caching my_scenes.py HeavyScene > time_profile.txt

# Run the parser to extract the hitlist and generate target_hitlist.txt
python parse_hitlist.py

# ---------------------------------------------------------
# STAGE 5: Graph Generation
# ---------------------------------------------------------
echo -e "\n[5/6] 📈 Generating Distribution Graphs..."
python visualize_energy.py

# ---------------------------------------------------------
# STAGE 6: Visual Verification Render (Golden Master Test)
# ---------------------------------------------------------
echo -e "\n[6/6] 🎬 Generating Golden Master Visual Verification Video..."
# Render exactly once, unprofiled, to visually certify output fidelity
python ../manim/__main__.py -qh --disable_caching my_scenes.py HeavyScene

# ---------------------------------------------------------
# STAGE 7: Cleanup & Packaging
# ---------------------------------------------------------
echo -e "\n🧹 Packaging experiment data..."

# Move all the generated files into the isolated experiment folder
mv baseline_energy.csv "$EXP_DIR/raw_energy_data.csv"
mv energy_baseline_plot.pdf "$EXP_DIR/distribution_plot.pdf"
mv time_profile.txt "$EXP_DIR/time_profile.txt"
mv target_hitlist.txt "$EXP_DIR/target_hitlist.txt"

# Route the visual verification video into the folder if it exists
LOCAL_VIDEO_PATH="media/videos/my_scenes/1080p60/HeavyScene.mp4"
if [ -f "$LOCAL_VIDEO_PATH" ]; then
    mv "$LOCAL_VIDEO_PATH" "$EXP_DIR/visual_verification.mp4"
    echo "🎬 Visual verification video packaged successfully."
else
    echo "⚠️ Warning: Could not locate verification video at $LOCAL_VIDEO_PATH"
fi

# If your analysis script generated a text summary, move it too
if [ -f "energy_results_summary.txt" ]; then
    mv energy_results_summary.txt "$EXP_DIR/summary.txt"
fi

echo -e "\n✅ Experiment Complete! All telemetry and visual artifacts securely packaged in: $EXP_DIR/"