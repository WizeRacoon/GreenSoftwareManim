import numpy as np
from manim.utils.bezier import interpolate as optimized_interpolate

# 1. The original, un-optimized function from the baseline
def original_interpolate(start, end, alpha):
    return (1 - alpha) * start + alpha * end

def test_interpolate_accuracy():
    print("Testing algebraic accuracy of optimized interpolate()...")
    
    # Generate some dummy spatial arrays similar to what Manim uses
    start_arrays = np.random.rand(1000, 3) # 1000 3D points
    end_arrays = np.random.rand(1000, 3)
    alphas = np.random.rand(1000, 1)       # 1000 alpha steps
    
    # Calculate using the old baseline method
    expected_output = original_interpolate(start_arrays, end_arrays, alphas)
    
    # Calculate using Teun and Mees's new method
    actual_output = optimized_interpolate(start_arrays, end_arrays, alphas)
    
    try:
        # np.testing will instantly fail if the arrays don't match exactly
        # (allowing for a tiny 1e-7 margin of floating-point rounding error)
        np.testing.assert_allclose(actual_output, expected_output, rtol=1e-7, atol=1e-7)
        print("✅ SUCCESS: The optimized function produces mathematically identical coordinates.")
    except AssertionError as e:
        print("❌ FAILURE: The optimized function altered the mathematical output!")
        print(e)

if __name__ == "__main__":
    test_interpolate_accuracy()