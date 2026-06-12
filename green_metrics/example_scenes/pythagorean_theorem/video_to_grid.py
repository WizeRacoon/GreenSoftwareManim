#!/usr/bin/env python3
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

def create_video_transformation_grid(video_path, output_path, timesteps):
    """
    Extracts 8 specific frames from an MP4 video based on user-defined 
    timestamps, crops 10% black margins from the sides, and compiles 
    the enlarged centers into a dense vertical 4x2 matrix grid.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    # Open video stream
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print("=========================================================")
    print("VIDEO PROFILER & KEYFRAME EXTRACTOR (4x2 VERTICAL MATRIX)")
    print("=========================================================")
    print(f"Source Video: {video_path}")
    print(f"Properties:   {duration:.2f} seconds | {total_frames} total frames @ {fps:.2f} FPS\n")

    # Guard check: Ensure we have exactly 8 timesteps for the 4x2 matrix
    if len(timesteps) != 8:
        raise ValueError(f"Matrix layout mismatch: Expected exactly 8 timestamps, received {len(timesteps)}.")

    # Initialize a 4x2 Matplotlib layout
    # Sized (7, 11) to balance the vertical elongation of 4 rows and 2 columns
    fig, axes = plt.subplots(4, 2, figsize=(7, 11))
    axes = axes.flatten()

    print("Extracting and cropping target transformations...")
    for idx, t in enumerate(timesteps):
        target_time = max(0.0, min(t, duration - 0.01))
        frame_idx = int(target_time * fps)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        success, frame = cap.read()
        
        if success:
            # 10% Side Margin Eradication & Center Crop
            h, w, _ = frame.shape
            crop_start = int(w * 0.10)  # Drop first 10% from the left
            crop_end = int(w * 0.90)    # Drop last 10% from the right
            cropped_frame = frame[:, crop_start:crop_end]
            
            # Convert BGR to RGB for accurate report visualization
            frame_rgb = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
            
            # Render enlarged frame on subplot axis
            axes[idx].imshow(frame_rgb)
            axes[idx].set_title(f"Timestamp: {target_time:.2f}s", fontsize=11, fontweight='bold', pad=4)
            print(f"  [Frame {idx+1:02d}/08] Cropped & Extracted frame index {frame_idx:04d} at {target_time:.2f}s")
        else:
            axes[idx].text(0.5, 0.5, "Frame\nRead Error", ha='center', va='center', color='red')
            print(f"  [Frame {idx+1:02d}/08] Error: Failed to extract frame at {target_time:.2f}s")
        
        axes[idx].axis('off')

    # Tight layout parameter settings to completely compress whitespace gaps
    fig.tight_layout(pad=0.1, h_pad=1.2, w_pad=0.1)
    
    print(f"\nCompiling print-ready dense grid...")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    cap.release()
    print(f"Success! 4x2 transformation matrix saved to: '{output_path}'")
    print("=========================================================")

if __name__ == "__main__":
    VIDEO_INPUT = "PythagoreanProof.mp4"
    IMAGE_OUTPUT = "pythagorean_transformation_grid.png"

    # Exactly 8 timesteps optimized for a 4x2 portrait sequence layout
    TARGET_TIMESTEPS = [
        0.5, 
        4.0, 4.4, 
        6.0, 9.2, 
        10.2, 11.2, 
        12.2
    ]

    create_video_transformation_grid(VIDEO_INPUT, IMAGE_OUTPUT, TARGET_TIMESTEPS)