#!/bin/bash
# run_benchmarks.sh

NUM_RUNS=30
echo "Starting $NUM_RUNS benchmark runs for statistical significance..."

# Clear out the old CSV if it exists so we start fresh
if [ -f baseline_energy.csv ]; then
    rm baseline_energy.csv
    echo "Cleared old baseline_energy.csv"
fi

for ((i=1; i<=NUM_RUNS; i++))
do
   echo "Run $i of $NUM_RUNS..."
   # This calls the benchmark.py wrapper we built earlier
   python benchmark.py
done

echo "Done! Data saved to baseline_energy.csv"