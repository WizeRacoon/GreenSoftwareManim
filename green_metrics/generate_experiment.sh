#!/bin/bash

# Ensure the user provided an experiment name
if [ -z "$1" ]; then
    echo "🛑 Error: No experiment name provided."
    echo "Usage: ./generate_experiment.sh <experiment_name>"
    echo "Example: ./generate_experiment.sh 01_baseline"
    echo "Example: ./generate_experiment.sh 02_numpy_arrays"
    exit 1
fi

EXP_NAME=$1

# This dynamically grabs the absolute path of the green_metrics folder
# no matter where you execute the script from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXP_DIR="$SCRIPT_DIR/experiments/$EXP_NAME"

echo "================================================="
echo " 🧪 Initializing Experiment: $EXP_NAME"
echo "================================================="

# Create the isolated experiment folder inside green_metrics/experiments/
mkdir -p "$EXP_DIR"

# ---------------------------------------------------------
# STAGE 1: The Safety Gateway
# ---------------------------------------------------------
echo -e "\n[1/5] 🛡️  Running Functionality & Safety Tests..."
python test_optimization.py

# The $? variable checks if the previous python script crashed or failed an assertion
if [ $? -ne 0 ]; then
    echo -e "\n❌ ABORT: Functionality test failed! The math is broken."
    echo "Fix the logic in bezier.py before running the energy benchmarks."
    # We delete the empty experiment folder so it doesn't clutter your workspace
    rm -r "$EXP_DIR" 
    exit 1
fi
echo "✅ Math checks passed. Proceeding to physical benchmarks."

# ---------------------------------------------------------
# STAGE 2: Energy Benchmarking
# ---------------------------------------------------------
echo -e "\n[2/5] ⚡ Running 30-Loop Energy Benchmarks..."
python benchmark.py

if [ $? -ne 0 ]; then
    echo -e "\n❌ ABORT: Benchmark failed. (Did you forget to unlock Intel RAPL?)"
    rm -r "$EXP_DIR"
    exit 1
fi

# ---------------------------------------------------------
# STAGE 3: Statistical Analysis
# ---------------------------------------------------------
echo -e "\n[3/5] 📊 Calculating Statistics..."
# Assuming analyze_energy.py generates energy_results_summary.txt
python analyze_energy.py 

# ---------------------------------------------------------
# STAGE 4: CPU Profiling
# ---------------------------------------------------------
echo -e "\n[4/5] ⏱️  Profiling CPU Time..."
python -m cProfile -s tottime ../manim/__main__.py -qh --disable_caching my_scenes.py HeavyScene > time_profile.txt

# Run the parser to extract the hitlist and generate target_hitlist.txt
python parse_hitlist.py

# ---------------------------------------------------------
# STAGE 5: Graph Generation
# ---------------------------------------------------------
echo -e "\n[5/5] 📈 Generating Distribution Graphs..."
python visualize_energy.py

# ---------------------------------------------------------
# STAGE 6: Cleanup & Packaging
# ---------------------------------------------------------
echo -e "\n🧹 Packaging experiment data..."

# Move all the generated files into the isolated experiment folder
mv baseline_energy.csv "$EXP_DIR/raw_energy_data.csv"
mv energy_baseline_plot.pdf "$EXP_DIR/distribution_plot.pdf"
mv time_profile.txt "$EXP_DIR/time_profile.txt"
mv target_hitlist.txt "$EXP_DIR/target_hitlist.txt"

# If your analysis script generated a text summary, move it too
if [ -f "energy_results_summary.txt" ]; then
    mv energy_results_summary.txt "$EXP_DIR/summary.txt"
fi

echo -e "\n✅ Experiment Complete! All data securely packaged in: $EXP_DIR/"