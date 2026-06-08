import numpy as np
import sys  # Added for sys.exit()
from manim.utils.bezier import interpolate as optimized_interpolate

def original_interpolate(start, end, alpha):
    return (1 - alpha) * start + alpha * end

def test_interpolate_accuracy():
    print("Testing algebraic accuracy of optimized interpolate()...")
    
    start_arrays = np.random.rand(1000, 3) 
    end_arrays = np.random.rand(1000, 3)
    alphas = np.random.rand(1000, 1)       
    
    expected_output = original_interpolate(start_arrays, end_arrays, alphas)
    actual_output = optimized_interpolate(start_arrays, end_arrays, alphas)
    
    try:
        np.testing.assert_allclose(actual_output, expected_output, rtol=1e-7, atol=1e-7)
        print("✅ SUCCESS: The optimized function produces mathematically identical coordinates.")
    except AssertionError as e:
        print("❌ FAILURE: The optimized function altered the mathematical output!")
        print(e)
        sys.exit(1) # <--- CRITICAL: Tells the bash pipeline to abort immediately!

def test_camera_smoke_render():
    print("\n🎥 Running camera smoke test (Functional Verification)...")
    try:
        from manim import Scene, Square, config
        
        class SmokeScene(Scene):
            def construct(self):
                square = Square().set_color("#2ca02c")
                self.add(square)
                self.wait(0.1)

        config.pixel_width = 160
        config.pixel_height = 90
        config.frame_rate = 15
        config.write_to_movie = False  
        
        scene = SmokeScene()
        scene.render()
        print("✅ SUCCESS: Camera code executed and rendered without runtime regressions.")
        
    except Exception as e:
        print("❌ FAILURE: Camera modifications caused a runtime crash!")
        raise e # <--- This naturally forces a non-zero exit code, so it's fine!

if __name__ == "__main__":
    test_interpolate_accuracy()
    test_camera_smoke_render()