#!/usr/bin/env bash
set -e

# Define your active manim core library paths
MANIM_DIR="$HOME/Downloads/GreenSoftwareManim/manim"
OPTIMIZATIONS_DIR="./manim_optimizations"
ITERATIONS=200  # Set to 200 for deep statistical significance overnight
CORES="2,3,4"   # Utilizing 3 physical cores for realistic parallelism

# Ensure RAPL energy readings are accessible before loop triggers
sudo chmod -R a+r /sys/class/powercap/intel-rapl/

echo "========================================================="
echo "STARTING ABLATION AUTOMATION (CORES: $CORES)"
echo "========================================================="

# Helper function to completely wipe all optimizations and restore the baseline
reset_to_baseline() {
    echo "--> Restoring all modules to Baseline (Original) state..."
    cp "${OPTIMIZATIONS_DIR}/transform/og_transform.py" "${MANIM_DIR}/animation/transform.py"
    cp "${OPTIMIZATIONS_DIR}/camera/og_camera.py" "${MANIM_DIR}/camera/camera.py"
    cp "${OPTIMIZATIONS_DIR}/three_d_camera/og_three_d_camera.py" "${MANIM_DIR}/camera/three_d_camera.py"
    cp "${OPTIMIZATIONS_DIR}/mobject/og_mobject.py" "${MANIM_DIR}/mobject/mobject.py"
    cp "${OPTIMIZATIONS_DIR}/vectorized_mobject/og_vectorized_mobject.py" "${MANIM_DIR}/mobject/types/vectorized_mobject.py"
    cp "${OPTIMIZATIONS_DIR}/bezier/og_bezier.py" "${MANIM_DIR}/utils/bezier.py"
    cp "${OPTIMIZATIONS_DIR}/simple_functions/og_simple_functions.py" "${MANIM_DIR}/utils/simple_functions.py"
    cp "${OPTIMIZATIONS_DIR}/space_ops/og_space_ops.py" "${MANIM_DIR}/utils/space_ops.py"
}

# ---------------------------------------------------------
# STAGE 1: Pure Baseline
# ---------------------------------------------------------
echo "[1/5] Setting up Stage 1: Pure Baseline..."
reset_to_baseline

echo "Running Baseline ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh f00_baseline $ITERATIONS

echo "Thermal cooldown sequence (30 seconds)..."
sleep 30

# ---------------------------------------------------------
# STAGE 2: Core Mobject Hierarchy Only
# ---------------------------------------------------------
echo "[2/5] Setting up Stage 2: Mobject DFS & Memory Allocation..."
reset_to_baseline
cp "${OPTIMIZATIONS_DIR}/mobject/optimized_mobject.py" "${MANIM_DIR}/mobject/mobject.py"
# Excluded vectorized_mobject here to isolate the DFS/Concatenate impact

echo "Running Mobject Hierarchy ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh f01_mobject_core $ITERATIONS

echo "Thermal cooldown sequence (30 seconds)..."
sleep 30

# ---------------------------------------------------------
# STAGE 3: Spatial & Math Engine Only
# ---------------------------------------------------------
echo "[3/5] Setting up Stage 3: Space Ops & Bezier Math..."
reset_to_baseline
cp "${OPTIMIZATIONS_DIR}/space_ops/optimized_space_ops.py" "${MANIM_DIR}/utils/space_ops.py"
cp "${OPTIMIZATIONS_DIR}/bezier/optimized_bezier.py" "${MANIM_DIR}/utils/bezier.py"

echo "Running Math Engine ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh f02_math_engine $ITERATIONS

echo "Thermal cooldown sequence (30 seconds)..."
sleep 30

# ---------------------------------------------------------
# STAGE 4: Camera & Projection Only
# ---------------------------------------------------------
echo "[4/5] Setting up Stage 4: 2D/3D Camera Vectorization..."
reset_to_baseline
cp "${OPTIMIZATIONS_DIR}/camera/optimized_camera.py" "${MANIM_DIR}/camera/camera.py"
cp "${OPTIMIZATIONS_DIR}/three_d_camera/optimized_three_d_camera.py" "${MANIM_DIR}/camera/three_d_camera.py"

echo "Running Camera System ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh f03_camera_system $ITERATIONS

echo "Thermal cooldown sequence (30 seconds)..."
sleep 30

# ---------------------------------------------------------
# STAGE 5: The Master Combined Run
# ---------------------------------------------------------
echo "[5/5] Setting up Stage 5: FULL GREEN OPTIMIZATION SUITE..."
# Copy all major optimizations
cp "${OPTIMIZATIONS_DIR}/mobject/optimized_mobject.py" "${MANIM_DIR}/mobject/mobject.py"
cp "${OPTIMIZATIONS_DIR}/space_ops/optimized_space_ops.py" "${MANIM_DIR}/utils/space_ops.py"
cp "${OPTIMIZATIONS_DIR}/bezier/optimized_bezier.py" "${MANIM_DIR}/utils/bezier.py"
cp "${OPTIMIZATIONS_DIR}/camera/optimized_camera.py" "${MANIM_DIR}/camera/camera.py"
cp "${OPTIMIZATIONS_DIR}/three_d_camera/optimized_three_d_camera.py" "${MANIM_DIR}/camera/three_d_camera.py"

# Add in the minor micro-optimizations for the aggregate run
cp "${OPTIMIZATIONS_DIR}/vectorized_mobject/optimized_vectorized_mobject.py" "${MANIM_DIR}/mobject/types/vectorized_mobject.py"
cp "${OPTIMIZATIONS_DIR}/transform/optimized_transform.py" "${MANIM_DIR}/animation/transform.py"
cp "${OPTIMIZATIONS_DIR}/simple_functions/optimized_simple_functions.py" "${MANIM_DIR}/utils/simple_functions.py"

echo "Running Full Combined Suite ($ITERATIONS Iterations)..."
taskset -c $CORES ./generate_experiment.sh f04_combined_master $ITERATIONS


echo "========================================================="
echo "ALL EXPERIMENTS COMPLETED SUCCESSFULLY"
echo "========================================================="