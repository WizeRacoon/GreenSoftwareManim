#!/usr/bin/env bash
set -e

# Define your active manim core library paths
MANIM_DIR="$HOME/Downloads/GreenSoftwareManim/manim"
OPTIMIZATIONS_DIR="./manim_optimizations"
ITERATIONS=200
CORES="2,3,4" # Utilizing 3 physical cores for realistic parallelism

# Ensure RAPL energy readings are accessible before loop triggers
sudo chmod -R a+r /sys/class/powercap/intel-rapl/

echo "========================================================="
echo "STARTING 4-STAGE ABLATION AUTOMATION RUN (CORES: $CORES)"
echo "========================================================="

# ---------------------------------------------------------
# STAGE 1: Baseline (Original Camera + Original Bezier)
# ---------------------------------------------------------
echo "[1/4] Setting up Stage 1: Pure Baseline..."
cp "${OPTIMIZATIONS_DIR}/camera/og_camera.py" "${MANIM_DIR}/camera.py"
cp "${OPTIMIZATIONS_DIR}/bezier/og_bezier.py" "${MANIM_DIR}/bezier.py"

echo "Running 00_baseline ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh 00_baseline_2 $ITERATIONS

echo "Cooling down CPU for 30 seconds..."
sleep 30

# ---------------------------------------------------------
# STAGE 2: Camera Optimization Only
# ---------------------------------------------------------
echo "[2/4] Setting up Stage 2: Camera Only..."
cp "${OPTIMIZATIONS_DIR}/camera/optimized_camera.py" "${MANIM_DIR}/camera.py"
cp "${OPTIMIZATIONS_DIR}/bezier/og_bezier.py" "${MANIM_DIR}/bezier.py"

echo "Running 01_camera_only ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh 01_camera_2 $ITERATIONS

echo "Cooling down CPU for 30 seconds..."
sleep 30

# ---------------------------------------------------------
# STAGE 3: Bezier Optimization Only
# ---------------------------------------------------------
echo "[3/4] Setting up Stage 3: Bezier Only..."
cp "${OPTIMIZATIONS_DIR}/camera/og_camera.py" "${MANIM_DIR}/camera.py"
cp "${OPTIMIZATIONS_DIR}/bezier/optimized_bezier.py" "${MANIM_DIR}/bezier.py"

echo "Running 02_bezier_only ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh 02_bezier_2 $ITERATIONS

echo "Cooling down CPU for 30 seconds..."
sleep 30

# ---------------------------------------------------------
# STAGE 4: Combined Optimizations (Camera + Bezier)
# ---------------------------------------------------------
echo "[4/4] Setting up Stage 4: Combined Optimizations..."
cp "${OPTIMIZATIONS_DIR}/camera/optimized_camera.py" "${MANIM_DIR}/camera.py"
cp "${OPTIMIZATIONS_DIR}/bezier/optimized_bezier.py" "${MANIM_DIR}/bezier.py"

echo "Running 03_combined ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh 03_combined_2 $ITERATIONS

echo "========================================================="
echo "ALL EXPERIMENTS COMPLETED SUCCESSFULLY"
echo "========================================================="