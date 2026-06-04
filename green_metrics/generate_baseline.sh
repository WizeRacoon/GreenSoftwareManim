#!/bin/bash
# generate_baseline.sh

echo "====================================="
echo "  Manim Green Software Test Suite"
echo "====================================="

# 1. Run the energy benchmarks (from your run_benchmarks.sh script)
echo -e "\n[1/4] Running Energy Benchmarks (This will take a few minutes)..."
./run_benchmarks.sh

# 2. Analyze the energy data and save the output
echo -e "\n[2/4] Calculating Energy Statistics..."
python analyze_energy.py > energy_results_summary.txt
cat energy_results_summary.txt

# 3. Run the time profiler for the hitlist
echo -e "\n[3/4] Profiling CPU Time (Single High-Quality Run)..."
python -m cProfile -s tottime -m manim -qh --disable_caching my_scenes.py HeavyScene > time_profile.txt

# 4. Parse the profiler data to create the hitlist
echo -e "\n[4/4] Generating Optimization Hitlist..."
python parse_hitlist.py > target_hitlist.txt
cat target_hitlist.txt

echo -e "\n====================================="
echo "  Pipeline Complete!"
echo "  Saved: baseline_energy.csv, energy_results_summary.txt,"
echo "         time_profile.txt, and target_hitlist.txt"
echo "====================================="